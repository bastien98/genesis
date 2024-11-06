"use client";

import { Fragment, useContext } from "react";
import { ConversationsContext } from "./providers/ConversationsProvider";
import Form from "./components/Form/Form";
import Messages from "./components/Messages/Messages";

export default function Home() {
    const { selectedChat } = useContext(ConversationsContext);

    return !selectedChat ? (
        <Form />
    ) : (
        <Fragment>
            <Messages />
            <Form />
        </Fragment>
    );
}
