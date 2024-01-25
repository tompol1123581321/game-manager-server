import { ObjectId } from "https://deno.land/x/mongo@v0.31.2/mod.ts";
import { Sha512 } from "../../deps.ts";
import { Session, User } from "../../models/index.ts";
import { getDbClient } from "../connectToDb.ts";

export const authorizeUser = async ({ password, username }: User) => {
  const dbClient = getDbClient("users");
  const matchedUserDocument = (await dbClient.findOne({
    username,
  })) as User;

  if (matchedUserDocument) {
    const hasher = new Sha512();
    const hashedPassword = hasher.update(password).toString();
    if (matchedUserDocument.password === hashedPassword) {
      return matchedUserDocument;
    }
  }
  throw new Error("Wrong username or password");
};

export const registerNewUser = async ({ password, username }: User) => {
  const dbClient = getDbClient("users");
  const isAlreadyExisting = await dbClient.findOne({ username });

  if (!isAlreadyExisting) {
    const hasher = new Sha512();
    const hashedPassword = hasher.update(password).toString();
    const newUser: User = {
      password: hashedPassword,
      username,
      purchasedGames: [],
      credit: 0,
    };
    await dbClient.insertOne(newUser);
    return newUser;
  } else {
    throw new Error("Acount with username already exists");
  }
};

export const addPurchasedGames = async (userId: string, gameId: string) => {
  const userDbClient = getDbClient("users");
  const gameDbClient = getDbClient("games");
  const gameQuery = { _id: new ObjectId(gameId) };
  const userQuery = { _id: new ObjectId(userId) };

  const selecetedGame = await gameDbClient.findOne(gameQuery);
  const selectedUser = await userDbClient.findOne(userQuery);
  const gamePrice = selecetedGame?.price;

  if (selectedUser?.credit < gamePrice) {
    throw new Error("Not enough credit");
  }

  const newValues = {
    $push: { purchasedGames: gameId },
    $inc: { credit: -gamePrice },
  };
  const { modifiedCount } = await userDbClient.updateOne(userQuery, newValues);

  if (modifiedCount !== 1) {
    throw new Error("Operation failed");
  }
  const updatedUser = await userDbClient.findOne(userQuery);
  return { updatedUser };
};

export const changeSessionState = async (
  userId: string,
  gameId: string,
  jwt: string,
  deactivate?: boolean
) => {
  const userDbClient = getDbClient("users");
  const userQuery = { _id: new ObjectId(userId) };
  const selectedUser = await userDbClient.findOne(userQuery);
  if (!selectedUser?.purchasedGames.includes(gameId) && !deactivate) {
    throw new Error("Game is not purchased");
  }
  const secret = crypto.randomUUID();
  const id = userId + "-" + gameId;
  const session: Session | undefined = deactivate
    ? undefined
    : {
        gameId,
        id,
        jwt,
        secret,
      };
  const newValues = {
    $set: { session },
  };
  const { modifiedCount } = await userDbClient.updateOne(userQuery, newValues);
  console.log({ modifiedCount, secret });
  return { secret };
};

export const validateSession = async (
  jwt: string,
  userId: string,
  gameId: string
) => {
  const userDbClient = getDbClient("users");
  const userQuery = { _id: new ObjectId(userId) };
  const selectedUser = await userDbClient.findOne(userQuery);
  const session: Session | undefined = selectedUser?.session;

  if (
    session?.gameId === gameId &&
    session?.id === userId + "-" + gameId &&
    session?.jwt === jwt
  ) {
    // await changeSessionState(userId,gameId,jwt,true)
    return { secret: session.secret };
  } else {
    console.log("gotten here 123");
    throw new Error("Operation failed");
  }
};
