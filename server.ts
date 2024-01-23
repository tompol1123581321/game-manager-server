import router from "./controllers/router.ts";
import { connectToDb } from "./db/connectToDb.ts";

import { Application, oakCors } from "./deps.ts";

await connectToDb();

const app = new Application();

app.use(
  oakCors({
    origin: "http://localhost:1420",
    allowedHeaders: [
      "Content-Type",
      "Authorization",
      "Access-Control-Allow-Credentials",
      "Set-Cookie",
    ],
    credentials: true,
    exposedHeaders: "*",
  })
);

app.use(router.routes());
app.use(router.allowedMethods());

const port = 8000;
console.log(`Server is running on http://localhost:${port}`);
await app.listen({ port });
