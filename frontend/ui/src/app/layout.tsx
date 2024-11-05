import type { Metadata } from "next";
import "./globals.css";
import { Poppins } from "next/font/google";
import Container from "./components/Container/Container";
import Header from "./components/Header/Header";
import Sidebar from "./components/Sidebar/Sidebar";
import Main from "./components/Main/Main";

const poppins = Poppins({
    subsets: ["latin"],
    weight: ["300", "400", "500", "600", "700"],
});

export const metadata: Metadata = {
    title: "Gilles Moenaert Software Project",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <body className={poppins.className}>
                <Container>
                    <Sidebar />
                    <Main>
                        <Header />
                        {children}
                    </Main>
                </Container>
            </body>
        </html>
    );
}
