import { Router } from "../../deps.ts";
import { authorized } from "../../middleware/isAuthorized.ts";
import { downloadGame, getAllGames } from "./gamesControllers.ts";

const router = new Router();

router.post("/api/downloadGame", authorized, downloadGame);
router.get("/api/getAllGames", authorized, getAllGames);

export default router;

//  write all user and game controllers
//  test it
//  work on client
