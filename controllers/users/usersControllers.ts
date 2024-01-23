import {
  addPurchasedGames,
  changeSessionState,
  authorizeUser,
  registerNewUser,
  validateSession,
} from "../../db/operations/index.ts";
import { RouterContext, create } from "../../deps.ts";
import { User } from "../../models/index.ts";
import {
  JWT_COOKIE_EXPIRATION,
  JWT_COOKIE_NAME,
  key,
} from "../../utils/authoriazationUtils.ts";

export const loginUser = async (ctx: RouterContext<string>) => {
  const authParameters: User = await ctx.request.body().value;

  try {
    const authorizedUser = await authorizeUser(authParameters);

    if (!authorizedUser) {
      ctx.response.body = { isAuthorized: false };
      ctx.response.status = 500;
    } else {
      const payload = {
        id: authorizedUser._id,
        name: authParameters.username,
      };
      const jwt = await create({ alg: "HS512", typ: "JWT" }, { payload }, key);

      const expirationDate = new Date(
        Date.now() + JWT_COOKIE_EXPIRATION * 1000
      );

      ctx.cookies.set(JWT_COOKIE_NAME, jwt, {
        expires: expirationDate,
        httpOnly: true,
        // secure: true,
        sameSite: "strict",
      });

      ctx.response.body = {
        isAuthorized: !!authorizeUser,
        token: jwt,
        authorizedUser,
      };
      ctx.response.status = 200;
    }
  } catch (error) {
    ctx.response.body = { isAuthorized: false, message: error.message };
    ctx.response.status = 500;
  }
};

export const registerUser = async (ctx: RouterContext<string>) => {
  try {
    const authParameters: User = await ctx.request.body().value;
    const authorizedUser = await registerNewUser(authParameters);
    if (!authorizedUser) {
      ctx.response.body = { isAuthorized: false };
      ctx.response.status = 500;
    } else {
      const payload = {
        id: authorizedUser._id,
        name: authParameters.username,
      };
      const jwt = await create({ alg: "HS512", typ: "JWT" }, { payload }, key);

      const expirationDate = new Date(
        Date.now() + JWT_COOKIE_EXPIRATION * 1000
      );

      ctx.cookies.set(JWT_COOKIE_NAME, jwt, {
        expires: expirationDate,
        httpOnly: true,
        sameSite: "strict",
      });
      ctx.response.body = { isAuthorized: true, token: jwt, authorizedUser };
      ctx.response.status = 200;
    }
  } catch (error) {
    ctx.response.body = { isAuthorized: false, message: error.message };
    ctx.response.status = 500;
  }
};

export const purchaseGame = async (ctx: RouterContext<string>) => {
  try {
    const requestBody = await ctx.request.body().value;
    console.log({ requestBody });
    const { updatedUser } = await addPurchasedGames(
      requestBody.userId,
      requestBody.gameId
    );
    ctx.response.status = 200;
    ctx.response.body = { updatedUser };
  } catch (error) {
    ctx.response.body = { message: error.message };
    ctx.response.status = 500;
  }
};

export const activateSession = async (ctx: RouterContext<string>) => {
  try {
    const { userId, gameId, jwt } = await ctx.request.body().value;
    const { secret } = await changeSessionState(userId, gameId, jwt);
    ctx.response.body = { secret };
    ctx.response.status = 200;

    setTimeout(async () => {
      await changeSessionState(userId, gameId, jwt, true);
    }, 2 * 60 * 1000 * 1000);
  } catch (error) {
    ctx.response.body = { message: error.message };
    ctx.response.status = 500;
  }
};

export const checkSessionValidity = async (ctx: RouterContext<string>) => {
  try {
    const { userId, gameId, jwt } = await ctx.request.body().value;
    const { secret } = await validateSession(jwt, userId, gameId);
    // await changeSessionState(userId, gameId, jwt, true);
    ctx.response.body = { secret };
    ctx.response.status = 200;
  } catch (error) {
    console.log("h", error);
    ctx.response.body = { message: error.message };
    ctx.response.status = 500;
  }
};
