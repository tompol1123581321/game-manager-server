import { Router } from "../../deps.ts";
import { authorized } from "../../middleware/isAuthorized.ts";
import {
  loginUser,
  purchaseGame,
  registerUser,
  activateSession,
  checkSessionValidity,
} from "./usersControllers.ts";

const router = new Router();

router.post("/api/login", loginUser);
router.post("/api/register", registerUser);
router.post("/api/purchaseGame", authorized, purchaseGame);
router.post("/api/activateSession", authorized, activateSession);
router.post("/api/checkSessionValidity", checkSessionValidity);

export default router;
