import api from "../config/api";

export const sendMessage = async (message: string) => {
  const res = await api.post("/chatbot/message", { message });
  return res.data;
};
