"use client";

import { useEffect, useState, useContext, Fragment } from "react";
import styles from "./Messages.module.css";
import { ConversationsContext } from "@/app/providers/ConversationsProvider";
import UserMessage from "./UserMessage";
import BotMessage from "./BotMessage";
import UserProfileModel from "../Header/UserProfileModel";

export default function Messages() {
    const { selectedChat, messages, setMessages } = useContext(ConversationsContext);
    const [userProfile, setUserProfile] = useState<UserProfileModel>();

    useEffect(() => {
        fetch(process.env.NEXT_PUBLIC_SERVER_URL + "/get_chat_messages/" + selectedChat)
            .then((res) => res.json())
            .then((data) => {
                setMessages(data);
            })
    }, [selectedChat]);

    useEffect(() => {
        fetch(process.env.NEXT_PUBLIC_SERVER_URL + "/get_profile")
            .then((res) => res.json())
            .then((data) => {
                setUserProfile(data);
            })
    }, []);

    /* There should be a socket.on listener here within a useEffect hook for a message_update websocket event
     * where the event should contain the message ID as well as its updated content, e.g.: 
     * {
     *      messageId: 1,
     *      textContent: "Hello, how can I he",
     * }
     * On every message_update event, the message with the matching ID should be updated. Since react is...well... reactive, any updates to the messages state (Done via setMessages method), should automatically cause the interface to re-render and show the updated content.
     */

    return selectedChat && (
        <div className={styles.messages}>
            {messages.length > 0 && messages.map((message) => {
                if (message.message_from === "User") {
                    return (
                        <Fragment key={message.id}>
                            <UserMessage text={message.text} sent_at={message.sent_at} userProfile={userProfile!} />
                        </Fragment>
                    );
                } else {
                    return (
                        <Fragment key={message.id}>
                            <BotMessage text={message.text} sent_at={message.sent_at} />
                        </Fragment>
                    )
                }
            })}
        </div>
    );
}
