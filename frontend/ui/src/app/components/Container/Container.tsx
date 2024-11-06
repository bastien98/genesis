"use client";

import { ConversationsProvider } from "@/app/providers/ConversationsProvider";
import styles from "./Container.module.css";

export default function Container({ children }: Readonly<{ children: React.ReactNode }>) {
    return (
        <div className={styles.container}>
            <ConversationsProvider>
                {children}
            </ConversationsProvider>
        </div>
    );
}
