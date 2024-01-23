import { Router } from "../deps.ts";
import gamesRouter from "./games/gamesRouter.ts";
import usersRouter from "./users/usersRouter.ts";

const router = new Router();

router.use(usersRouter.routes());
router.use(usersRouter.allowedMethods());

router.use(gamesRouter.routes());
router.use(gamesRouter.allowedMethods());

export default router;
