export type User = {
  _id?: string;
  password: string;
  username: string;
  purchasedGames: Array<string>;
  credit: number;
  session?: Session;
};
export type Game = {
  _id: string;
  name: string;
  price: number;
  description: string;
  imageUrl: string;
};

export type Session = {
  id: string;
  gameId: string;
  jwt: string;
  secret: string;
};
