import UserProfileModel from "../Header/UserProfileModel";
import styles from "./Messages.module.css";

interface Message {
    text: string;
    sent_at: number;
    userProfile: UserProfileModel;
}

export default function UserMessage({ text, sent_at, userProfile }: Message) {
    return (
        <div className={styles.userMessage}>
            <div className={styles.pfp} style={{ display: "none" }}>
                {userProfile && <img
                    src={process.env.NEXT_PUBLIC_SERVER_URL + userProfile.image}
                    alt="user profile picture"
                />}
            </div>
            <div className={styles.message}>
                <span>{text}</span>
            </div>
            <div className={styles.messageMetaData} style={{ display: "none" }}>
                Me &#x2022; {new Date(sent_at * 1000).getHours() + ":" + new Date(sent_at * 1000).getMinutes()}
            </div>
        </div>
    );
}
