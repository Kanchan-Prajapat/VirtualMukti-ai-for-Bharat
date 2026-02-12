import api from "../config/api";

export const login = async (username: string, password: string) => {
  const res = await api.post("/auth/login", { username, password });
  return res.data;
};

export const register = async (data: any) => {
  const res = await api.post("/auth/register", data);
  return res.data;
};
