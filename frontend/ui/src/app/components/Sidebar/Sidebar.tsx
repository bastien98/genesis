"use client";

import { useEffect, useState, useContext } from "react";
import KnowledgeBaseSelectBox from "../KnowledgeBaseSelectBox/KnowledgeBaseSelectBox";
import styles from "./Sidebar.module.css";
import { nanoid } from "nanoid";
import { ConversationsContext } from "@/app/providers/ConversationsProvider";
import useWindowDimensions from "@/app/helpers/useWindowDimensions";

export default function Sidebar() {
    const [selectedKnowledgeBase, setSelectedKnowledgeBase] = useState<string>();
    const [chatsTimeCategories, setChatsTimeCategories] = useState<string[]>([]);
    const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
    const { chats, setChats, originalChats, setOriginalChats, setSelectedChat, setMessages } = useContext(ConversationsContext);
    const [ width ] = useWindowDimensions();

    useEffect(() => {
        fetch(process.env.NEXT_PUBLIC_SERVER_URL + "/get_chats")
            .then((res) => res.json())
            .then((data) => {
                setOriginalChats(data);
                setChats(data);
            })

    }, []);

    useEffect(() => {
        fetch(process.env.NEXT_PUBLIC_SERVER_URL + "/get_knowledge_bases?user_id=1")
            .then((res) => res.json())
            .then((data) => {
                setSelectedKnowledgeBase(data[0].title);
            })
    }, []);

    useEffect(() => {
        if (chats.length > 0) {
            const categories = new Set<string>();

            chats.forEach((chat) => {
                categories.add(chat.time_category);
            });

            setChatsTimeCategories(Array.from(categories));
        }
    }, [chats]);

    useEffect(() => {
        setChats(originalChats);
    }, [originalChats]);

    useEffect(() => {
        if (selectedKnowledgeBase) {
            console.log(originalChats)
            console.log(selectedKnowledgeBase)
            setChats(originalChats.filter((chat) => chat.knowledge_base == selectedKnowledgeBase));
        }
    }, [selectedKnowledgeBase, originalChats]);

    const onDelete = (id: number) => {
        fetch(process.env.NEXT_PUBLIC_SERVER_URL + "/delete_chat/" + id.toString(), {
            method: "GET",
        }).then((response) => {
            if (response.status === 200) {
                response.json().then((data) => {
                    setOriginalChats(data.chats);
                    setMessages(data.chat_messages);
                });
            }
        })
    }

    useEffect(() => {
        if (width < 1024) {
            setSidebarCollapsed(true);
        }
    }, []);

    return (
        <div className={`${styles.sidebar} ${sidebarCollapsed ? styles.sidebarCollapsed : ""}`}>
            <div className={styles.sidebarHeader}>
                <button onClick={() => setSidebarCollapsed(!sidebarCollapsed)}>
                    <svg width="36" height="36" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M4.5 27V24H31.5V27H4.5ZM4.5 19.5V16.5H31.5V19.5H4.5ZM4.5 12V9H31.5V12H4.5Z" fill="#262831" />
                    </svg>
                </button>
                {!sidebarCollapsed && <KnowledgeBaseSelectBox onChange={setSelectedKnowledgeBase} />}
            </div>
            {!sidebarCollapsed && <div className={`${styles.sidebarChats}`}>
                {
                    chatsTimeCategories.map((timeCategory) => {
                        return (
                            <div key={nanoid(8)}>
                                <p className={styles.sidebarTimeCategory}>{timeCategory}</p>
                                {
                                    chats
                                        .filter((chat) => chat.time_category === timeCategory)
                                        .map((chat) => {
                                            return (
                                                <div
                                                    key={chat.id + "_chat"}
                                                    className={styles.sidebarChat}
                                                    onClick={() => {
                                                        setSelectedChat(chat.id.toString());
                                                    }}
                                                >
                                                    <p>{chat.title}</p>
                                                    <button onClick={(e) => { e.stopPropagation(); onDelete(chat.id); }}>
                                                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                                            <path d="M7 21C6.45 21 5.97933 20.8043 5.588 20.413C5.19667 20.0217 5.00067 19.5507 5 19V6H4V4H9V3H15V4H20V6H19V19C19 19.55 18.8043 20.021 18.413 20.413C18.0217 20.805 17.5507 21.0007 17 21H7ZM17 6H7V19H17V6ZM9 17H11V8H9V17ZM13 17H15V8H13V17Z" fill="#262831" />
                                                        </svg>
                                                    </button>
                                                </div>
                                            );
                                        })
                                }
                            </div>
                        )
                    })
                }
            </div>
            }
        </div>
    );
}
