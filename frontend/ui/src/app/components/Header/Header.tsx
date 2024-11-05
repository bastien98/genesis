"use client";

import { useContext, useEffect, useState } from "react";
import styles from "./Header.module.css";
import UserProfileModel from "./UserProfileModel";
import { ConversationsContext } from "@/app/providers/ConversationsProvider";

export default function Header() {
    const [userProfile, setUserProfile] = useState<UserProfileModel>();
    const { selectedChat, setSelectedChat } = useContext(ConversationsContext);

    useEffect(() => {
        fetch(process.env.NEXT_PUBLIC_SERVER_URL + "/get_profile")
            .then((res) => res.json())
            .then((data) => {
                setUserProfile(data);
            });
    }, []);

    return userProfile && (
        <div className={styles.header}>
            <div className={styles.profile}>
                <img
                    src={process.env.NEXT_PUBLIC_SERVER_URL + userProfile.image}
                    alt={userProfile.username}
                />
                <span>
                    {userProfile.username}
                </span>
            </div>
            <button className="btnPrimary" disabled={!selectedChat} onClick={() => setSelectedChat(undefined)}>
                <div className="icon">
                    <svg width="27" height="27" viewBox="0 0 27 27" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12.375 14.625H5.625V12.375H12.375V5.625H14.625V12.375H21.375V14.625H14.625V21.375H12.375V14.625Z" fill="#F2F2F2" />
                    </svg>
                </div>
                NEW CHAT
            </button>
        </div>
    );
}
