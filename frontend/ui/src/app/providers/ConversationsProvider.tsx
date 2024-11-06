import React, { createContext, useState } from "react";
import ConversationModel from "./ConversationModel";
import MessageModel from "./MessageModel";

export const ConversationsContext = createContext<{
    selectedChat: string | undefined;
    originalChats: ConversationModel[];
    messages: MessageModel[];
    chats: ConversationModel[];
    setSelectedChat: React.Dispatch<React.SetStateAction<string | undefined>>;
    setChats: React.Dispatch<React.SetStateAction<ConversationModel[]>>
    setOriginalChats: React.Dispatch<React.SetStateAction<ConversationModel[]>>
    setMessages: React.Dispatch<React.SetStateAction<MessageModel[]>>
}>({
    selectedChat: undefined,
    setSelectedChat: () => { },
    originalChats: [],
    chats: [],
    setChats: () => { },
    setOriginalChats: () => { },
    messages: [],
    setMessages: () => { }
});

export const ConversationsProvider = ({ children }: { children: any }) => {
    const [selectedChat, setSelectedChat] = useState<string>();
    const [originalChats, setOriginalChats] = useState<ConversationModel[]>([]);
    const [chats, setChats] = useState<ConversationModel[]>([]);
    const [messages, setMessages] = useState<MessageModel[]>([]);

    return (
        <ConversationsContext.Provider
            value={{
                selectedChat,
                setSelectedChat,
                originalChats,
                chats,
                setChats,
                setOriginalChats,
                messages,
                setMessages
            }}>
            {children}
        </ConversationsContext.Provider>
    );
};
