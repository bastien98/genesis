"use client";

import { useContext, useEffect, useState } from "react";
import styles from "./Form.module.css";
import { ConversationsContext } from "@/app/providers/ConversationsProvider";
import KnowledgeBaseSelectBox from "../KnowledgeBaseSelectBox/KnowledgeBaseSelectBox";

export default function Form() {
    const { selectedChat, setSelectedChat, setMessages, setOriginalChats } = useContext(ConversationsContext);
    const [selectedKnowledgeBase, setSelectedKnowledgeBase] = useState<string>();

    useEffect(() => {
        fetch(process.env.NEXT_PUBLIC_SERVER_URL + "/get_knowledge_bases")
            .then((res) => res.json())
            .then((data) => {
                setSelectedKnowledgeBase(data[0].title);
            })
    }, []);

    const onSubmit = (e: any) => {
        e.preventDefault();

        const message = e.target.message.value;
        e.target.message.value = "";

        if (message.value != "" && !selectedChat) {
            fetch(process.env.NEXT_PUBLIC_SERVER_URL + "/new_chat/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ user_message: message, knowledge_base: selectedKnowledgeBase })
            }).then((response) => {
                if (response.status === 200) {
                    response.json().then((data) => {
                        setOriginalChats(data.chats)
                        setSelectedChat(data.chats.length.toString());
                        setMessages(data.chat_messages);
                    });
                }
            })
        } else if (message.value != "" && selectedChat) {
            fetch(process.env.NEXT_PUBLIC_SERVER_URL + "/new_message", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ user_message: message, chat_id: selectedChat })
            }).then((response) => {
                if (response.status === 200) {
                    response.json().then(() => {
                        setMessages((messages) => [
                            ...messages,
                            {
                                text: message,
                                sent_at: Math.round(Date.now() / 1000),
                                chat_id: parseInt(selectedChat),
                                id: messages.length + 1,
                                message_from: "User"
                            },
                        ]);
                    });
                }
            })
        }
    }

    return (
        <div className={`${styles.formContainer} ${!selectedChat && styles.showLightingEffect}`}>
            {!selectedChat && <h1 className={styles.title}>What can I help you with?</h1>}
            <form className={styles.form} onSubmit={onSubmit} style={{
                flexDirection: "column",
            }}>
                {!selectedChat && <div style={{ zIndex: "10", width: "250px" }}>
                    <KnowledgeBaseSelectBox onChange={setSelectedKnowledgeBase} />
                </div>}
                <div className={styles.form}>
                    <input
                        type="text"
                        placeholder="Type Message..."
                        className={styles.input}
                        id="message"
                    />
                    <button className={styles.sendBtn}>
                        <svg width="28" height="28" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path fillRule="evenodd" clipRule="evenodd" d="M20.9896 7.01167L6.29889 12.3235L11.1931 15.1562L15.5086 10.8395C15.7275 10.6207 16.0243 10.4979 16.3338 10.498C16.6433 10.4981 16.94 10.6212 17.1588 10.8401C17.3776 11.059 17.5004 11.3559 17.5003 11.6653C17.5002 11.9748 17.3771 12.2716 17.1582 12.4903L12.8416 16.807L15.6766 21.7L20.9896 7.01167ZM21.3664 4.39367C22.7606 3.8885 24.1116 5.2395 23.6064 6.63367L17.4441 23.6728C16.9377 25.0705 15.0291 25.2408 14.2836 23.954L10.5304 17.4697L4.04606 13.7165C2.75922 12.971 2.92956 11.0623 4.32722 10.556L21.3664 4.39367Z" fill="#F2F2F2" />
                        </svg>
                    </button>
                </div>
            </form>
        </div>
    );
}
