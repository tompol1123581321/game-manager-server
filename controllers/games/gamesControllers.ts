import {
  checkForDownloadGame,
  getAllPossibleGames,
} from "../../db/operations/index.ts";

import { RouterContext, join, send } from "../../deps.ts";

export const getAllGames = async (ctx: RouterContext<string>) => {
  try {
    const allGames = await getAllPossibleGames();
    ctx.response.status = 200;
    ctx.response.body = allGames;
  } catch (error) {
    ctx.response.status = 500;
    ctx.response.body = error.message;
  }
};

export const downloadGame = async (ctx: RouterContext<string>) => {
  try {
    const requestBody = await ctx.request.body().value;

    const checkResponse = await checkForDownloadGame(
      requestBody.gameId,
      requestBody.userId
    );
    console.log(checkResponse);

    if (checkResponse) {
      const zipFilePath = join(Deno.cwd(), "games", `${requestBody.gameId}.zip`);

      if (!(await Deno.stat(zipFilePath).catch(() => null))) {
        ctx.response.status = 404;
        ctx.response.body = { error: "File not found" };
        return;
      }
      await send(ctx, zipFilePath, {
        root: "/",
      });
    }
  } catch (e) {
    console.log(e);
    ctx.response.status = 404;
    ctx.response.body = { error: "Not Found" };
  }
};
