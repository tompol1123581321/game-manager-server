import { ObjectId } from "https://deno.land/x/mongo@v0.31.2/mod.ts";
import { Game } from "../../models/index.ts";
import { getDbClient } from "../connectToDb.ts";

export const getAllPossibleGames = async () => {
  const gameDbClient = getDbClient("games");
  const gameList = (await gameDbClient.find().toArray()) as Array<Game>;
  return gameList;
};

export const checkForDownloadGame = async (gameId: string, userId: string) => {
  const userDbClient = getDbClient("users");
  const userQuery = { _id: new ObjectId(userId) };
  const selectedUser = await userDbClient.findOne(userQuery);
  if (!selectedUser?.purchasedGames.includes(gameId)) {
    throw new Error("Game is not purchased");
  }
  return { gameId };
};

export const addMockGames = async () => {
  const gameDbClient = getDbClient("games");
  const mockGames: Array<Omit<Game, "_id">> = [
    {
      description: "Best game of 2024",
      imageUrl:
        "https://imgs.search.brave.com/3_-svRWFauQwgjnKDQs6Pl2NMY1qQuGSu555qP-PAdg/rs:fit:860:0:0/g:ce/aHR0cHM6Ly90My5m/dGNkbi5uZXQvanBn/LzAzLzc1LzQwLzEy/LzM2MF9GXzM3NTQw/MTI1OF9jSEhzT3hW/RFNjSTNMd2N1RkMz/NkU1RXVFc2tSWXNv/MC5qcGc",
      name: "RavenSuperGame",
      price: 0,
    },
    {
      description: "Best game of 2022",
      imageUrl:
        "https://imgs.search.brave.com/7B0aP3_-3mDCKm2qUfA_iPBz-9OGlCtpOlHeGMGIbuc/rs:fit:860:0:0/g:ce/aHR0cHM6Ly90NC5m/dGNkbi5uZXQvanBn/LzAxLzM1Lzc4LzY5/LzM2MF9GXzEzNTc4/Njk1Ml9HWTNWTHNo/WlhGRHpKdWhTMDJU/NHJUOHRDZDk4ZVdp/ay5qcGc",
      name: "Mock 1",
      price: 300,
    },
    {
      description: "Best game of 2023",
      imageUrl:
        "https://imgs.search.brave.com/jftqqHbYYJkVdJRgsgvXww7Kp9TCaDWt-0XhWkuIMks/rs:fit:860:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5pc3RvY2twaG90/by5jb20vaWQvNjI2/NDY0MTU4L3Bob3Rv/L2NhdC13aXRoLW9w/ZW4tbW91dGguanBn/P3M9NjEyeDYxMiZ3/PTAmaz0yMCZjPVFy/OURDVmt3S21fZHpm/amtlTjVmb0NCcDdj/M0VmQkZfaTJBMGV0/WWlKT0E9",
      name: "Mock 2",
      price: 400,
    },
  ];
  await gameDbClient.insertMany(mockGames);
};
