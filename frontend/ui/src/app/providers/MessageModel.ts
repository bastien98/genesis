export default interface MessageModel {
    id: number;
    chat_id: number;
    text: string;
    message_from: "User" | "Bot",
    sent_at: number;
}
