import { Context, verify, Next } from "../deps.ts";
import { key } from "../utils/authoriazationUtils.ts";

export const authorized = async (ctx: Context, next: Next) => {
  try {
    const headers: Headers = ctx.request.headers;
    const authorization = headers.get("Authorization");
    if (!authorization) {
      ctx.response.status = 401;
      return;
    }
    const jwt = authorization.split(" ")[1];
    console.log("from headers", String(jwt).trim().length);

    const tokenFromCookies = await ctx.cookies.get("authorization_jwt");
    console.log("from coocies", String(tokenFromCookies)?.trim());

    const payload = await verify(jwt, key);
    console.log(String(jwt).trim() === String(tokenFromCookies)?.trim());

    if (!jwt || jwt.trim() !== tokenFromCookies?.trim() || !payload) {
      ctx.response.status = 401;
      ctx.response.body = "Invalid JWT token";
      return;
    }

    await next();
  } catch {
    ctx.response.status = 401;
    ctx.response.body = "Invalid token";
  }
};
