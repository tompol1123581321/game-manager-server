import { MongoClient, load, Database } from "../deps.ts";
const env = await load();
const connectToDbString = env["DB_AUTH_STRING"];

type DBCollections = "users" | "games";

const client = new MongoClient();

let dbClient: Database;
const connectToDb = async () => {
  try {
    dbClient = await client.connect(connectToDbString);
    console.log("successfully connected to DB");
  } catch (error) {
    console.log("connection failed", error);
    throw new Error("Connection to db failed");
  }
};

const getDbClient = (collectionName: DBCollections) => {
  if (!dbClient) {
    throw new Error("No connection to DB");
  }
  return dbClient.collection(collectionName);
};

export { connectToDb, getDbClient };
