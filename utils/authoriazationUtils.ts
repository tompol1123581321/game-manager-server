import { RouterContext, create } from "../deps.ts";

export const key = await crypto.subtle.generateKey(
  { name: "HMAC", hash: "SHA-512" },
  true,
  ["sign", "verify"]
);

export const JWT_COOKIE_NAME = "authorization_jwt"; // Replace with your desired cookie name
export const JWT_COOKIE_EXPIRATION = 3600; // Expiration time in seconds (1 hour in this example)

type Payload = { id: string; name: string };

export const createJwtToken = async (payload: Payload) => {
  const jwtToken = await create({ alg: "HS512", typ: "JWT" }, { payload }, key);
  return jwtToken;
};

export const withAuthorization = async <ReturnType>(
  ctx: RouterContext<string>,
  routeFunction: (ctx: RouterContext<string>) => Promise<ReturnType>
) => {
  const { token }: { token: string } = await await ctx.request.body().value;
  const tokensFromCoocies = await ctx.cookies.get("authorization_jwt");
  if (token === tokensFromCoocies) {
    return await routeFunction(ctx);
  }
  ctx.response.body = { isAuthorized: false };
  ctx.response.status = 500;
  return;
};
