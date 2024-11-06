import styles from "./Messages.module.css";
import Markdown from "react-markdown";
import remarkGfm from 'remark-gfm'


interface Message {
    text: string;
    sent_at: number;
}

export default function BotMessage({ text, sent_at }: Message) {
    return (
        <div className={styles.botMessage}>
            <div className={styles.pfp}>
                <img src="/alien-logo.png" alt="Icon" width="38" height="38" />
            </div>
            <div className={styles.messageBoxShadow}>
                <div className={styles.message}>
                    <div>
                        <Markdown remarkPlugins={[remarkGfm]}>{text}</Markdown>
                    </div>
                </div>
            </div>
            <div className={styles.messageMetaData} style={{ display: "none" }}>
                {process.env.NEXT_PUBLIC_CHATBOT_NAME} &#x2022; {new Date(sent_at * 1000).getHours() + ":" + new Date(sent_at * 1000).getMinutes()}
            </div>
        </div>
    );
}
