import styles from "./Main.module.css";

export default function Main({ children }: Readonly<{ children: React.ReactNode }>) {
    return (
        <div className={styles.main}>
            {children}
        </div>
    );
}
