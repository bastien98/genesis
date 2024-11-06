chats = [
    {
        "id": 1,
        "title": "Are spaghettis and spaghettios similar things?",
        "time_category": "Today",
        "updated_at": 1730577770,
        "knowledge_base": "Cooking",
    },
    {
        "id": 2,
        "title": "What is the difference between a list and a set?",
        "time_category": "Today",
        "updated_at": 1730577770,
        "knowledge_base": "Technology",
    },
    {
        "id": 3,
        "title": "Harry Potter vs Lord of the Rings comparison.",
        "time_category": "Yesterday",
        "updated_at": 1730473370,
        "knowledge_base": "Gaming",
    },
]

chat_messages = [
    {
        "id": 1,
        "chat_id": 1,
        "text": "Are spaghettis and spaghettios the same?",
        "message_from": "User",
        "sent_at": 1730579462,
    },
    {
        "id": 2,
        "chat_id": 1,
        "text": "Yes, spaghettis and spaghettios are similar things.",
        "message_from": "Bot",
        "sent_at": 1730579462,
    },
    {
        "id": 3,
        "chat_id": 1,
        "text": "YAYYY!",
        "message_from": "User",
        "sent_at": 1730579462,
    },
    {
        "id": 4,
        "chat_id": 1,
        "text": "Glad I could help!",
        "message_from": "Bot",
        "sent_at": 1730579462,
    },
    {
        "id": 5,
        "chat_id": 2,
        "text": "What is the difference between a list and a set?",
        "message_from": "User",
        "sent_at": 1730579462,
    },
    {
        "id": 6,
        "chat_id": 2,
        "text": "A list is an ordered collection of items, while a set is an unordered collection of unique items.",
        "message_from": "Bot",
        "sent_at": 1730579462,
    },
    {
        "id": 7,
        "chat_id": 2,
        "text": "YASSS I WAS RIGHT!",
        "message_from": "User",
        "sent_at": 1730579462,
    },
    {
        "id": 8,
        "chat_id": 2,
        "text": "Glad I could help! Feel free to learn more.",
        "message_from": "Bot",
        "sent_at": 1730579462,
    },
    {
        "id": 9,
        "chat_id": 3,
        "text": "Harry Potter vs Lord of the Rings comparison.",
        "message_from": "User",
        "sent_at": 1730579462,
    },
    {
        "id": 10,
        "chat_id": 3,
        "text": """
# Plot Comparison: Harry Potter vs The Lord of the Rings

| **Aspect**               | **Harry Potter**                               | **The Lord of the Rings**                          |
|--------------------------|------------------------------------------------|---------------------------------------------------|
| **Main Protagonist**      | Harry Potter                                   | Frodo Baggins                                     |
| **Setting**               | Magical Britain, centered around Hogwarts      | Middle-earth, with various kingdoms and realms    |
| **Central Conflict**      | Harry vs. Voldemort                            | Frodo vs. Sauron                                  |
| **Main Objective**        | To defeat Lord Voldemort and bring peace to the magical world | To destroy the One Ring and defeat Sauron         |
| **Mentor Figure**         | Albus Dumbledore                               | Gandalf                                           |
| **Companions**            | Hermione Granger, Ron Weasley, and others      | Samwise Gamgee, Aragorn, Legolas, Gimli, and others|
| **Dark Lord**             | Voldemort                                      | Sauron                                            |
| **Magical Object**        | Elder Wand, Horcruxes                          | One Ring                                          |
| **Prophecy**              | Foretells Harry as the one with the power to defeat Voldemort | No prophecy directly tied to Frodo, but there is a sense of destiny regarding the Ring |
| **Key Themes**            | Friendship, courage, love, good vs evil, growing up | Friendship, loyalty, power, corruption, sacrifice |
| **Power Struggle**        | Wizards vs. Dark Wizards (Death Eaters)        | Free Peoples of Middle-earth vs. Sauron and his armies |
| **Villain’s Goal**        | To gain immortality and rule over the wizarding and non-wizarding world | To regain his full power and dominate all of Middle-earth |
| **Sacrifice**             | Harry willingly sacrifices himself to defeat Voldemort | Frodo risks his life to destroy the Ring, ultimately losing part of his identity |
| **Resolution**            | Voldemort is defeated, and peace is restored to the magical world | The One Ring is destroyed, Sauron is vanquished, and peace returns to Middle-earth |

### Key Similarities:
- **Epic Battles**: Both series include large-scale battles between forces of good and evil.
- **The Chosen One**: Both Harry and Frodo are reluctant heroes burdened with the task of saving their world.
- **Loyal Companions**: Harry has Ron and Hermione, while Frodo has Sam. Both series emphasize the importance of friendship.
- **Ultimate Evil**: Both Voldemort and Sauron are embodiments of evil, seeking to dominate the world.

### Key Differences:
- **World Complexity**: The Lord of the Rings presents a more expansive and detailed world (Middle-earth) with multiple races and deep history, while Harry Potter focuses more on the magical world existing parallel to the real world.
- **Tone**: Harry Potter has a more contemporary and sometimes lighthearted tone (especially early on), while The Lord of the Rings maintains a more serious and mythic tone throughout.
- **Magical Items**: In Harry Potter, magical items (wands, Horcruxes) are tools of power, while in The Lord of the Rings, the One Ring is a corruptive force that must be destroyed rather than used.

### Conclusion:
Both Harry Potter and The Lord of the Rings share common fantasy elements, such as the struggle between good and evil, magical artifacts, and the journey of a young hero. However, they differ in scope, tone, and the nature of the worlds they create. While Harry Potter is centered around a school and the development of its protagonist into adulthood, The Lord of the Rings deals with themes of ancient evil, sacrifice, and the larger fate of entire civilizations.
        """,
        "message_from": "Bot",
        "sent_at": 1730579462,
    },
    {
        "id": 11,
        "chat_id": 3,
        "text": "YAYYY!",
        "message_from": "User",
        "sent_at": 1730579462,
    },
    {
        "id": 12,
        "chat_id": 3,
        "text": "Glad I could help!",
        "message_from": "Bot",
        "sent_at": 1730579462,
    }
]

knowledge_bases = [
    {
        "id": 1,
        "title": "Gaming",
        "icon": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M7.49977 11.5V14.5M5.99977 13H8.99977M11.9998 3.782V8.124M14.8738 13H17.8738M11.9998 8.347C14.0048 8.347 15.6998 6.459 17.7858 7.135C20.0498 7.868 21.6058 10.548 21.4938 16.627C21.4718 17.851 21.1578 19.205 19.9478 19.733C17.1508 20.954 15.5508 17.405 12.9478 17.405H11.0508C8.44577 17.405 6.83777 20.95 4.05277 19.733C2.84277 19.205 2.52777 17.851 2.50577 16.626C2.39277 10.548 3.94977 7.868 6.21377 7.135C8.29877 6.459 9.99377 8.347 11.9998 8.347Z" stroke="#262831" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    },
    {
        "id": 2,
        "title": "Cooking",
        "icon": '<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M1.6725 2.45125C1.86875 1.7025 2.55125 1.25 3.26875 1.25C3.71125 1.25 4.11375 1.41625 4.42 1.6875C4.75765 1.40427 5.18428 1.24902 5.625 1.24902C6.06572 1.24902 6.49235 1.40427 6.83 1.6875C7.14684 1.40498 7.55674 1.24921 7.98125 1.25C8.69875 1.25 9.38125 1.7025 9.5775 2.45125C9.765 3.16625 10 4.31875 10 5.625C9.99997 6.35444 9.81755 7.07231 9.46934 7.71327C9.12113 8.35424 8.61818 8.89797 8.00625 9.295C7.6675 9.51625 7.5 9.80125 7.5 10.045V10.54C7.5 10.5683 7.50167 10.5958 7.505 10.6225C7.5475 10.9325 7.70125 12.0837 7.845 13.2775C7.98625 14.4487 8.125 15.7262 8.125 16.25C8.125 16.913 7.86161 17.5489 7.39277 18.0178C6.92393 18.4866 6.28804 18.75 5.625 18.75C4.96196 18.75 4.32607 18.4866 3.85723 18.0178C3.38839 17.5489 3.125 16.913 3.125 16.25C3.125 15.725 3.26375 14.45 3.405 13.2775C3.54875 12.0837 3.7025 10.9325 3.745 10.6225L3.75 10.54V10.045C3.75 9.80125 3.5825 9.51625 3.24375 9.295C2.63182 8.89797 2.12887 8.35424 1.78066 7.71327C1.43245 7.07231 1.25003 6.35444 1.25 5.625C1.25 4.31875 1.485 3.16625 1.6725 2.45125ZM7.5 6.25C7.5 6.41576 7.43415 6.57473 7.31694 6.69194C7.19973 6.80915 7.04076 6.875 6.875 6.875C6.70924 6.875 6.55027 6.80915 6.43306 6.69194C6.31585 6.57473 6.25 6.41576 6.25 6.25V3.125C6.25 2.95924 6.18415 2.80027 6.06694 2.68306C5.94973 2.56585 5.79076 2.5 5.625 2.5C5.45924 2.5 5.30027 2.56585 5.18306 2.68306C5.06585 2.80027 5 2.95924 5 3.125V6.25C5 6.41576 4.93415 6.57473 4.81694 6.69194C4.69973 6.80915 4.54076 6.875 4.375 6.875C4.20924 6.875 4.05027 6.80915 3.93306 6.69194C3.81585 6.57473 3.75 6.41576 3.75 6.25V2.98125C3.75 2.85361 3.6993 2.73121 3.60905 2.64095C3.51879 2.5507 3.39639 2.5 3.26875 2.5C3.06125 2.5 2.91875 2.62375 2.88125 2.76875C2.63491 3.70108 2.50683 4.6607 2.5 5.625C2.49994 6.1463 2.63029 6.65932 2.87918 7.11737C3.12807 7.57541 3.48759 7.96391 3.925 8.2475C4.47375 8.60375 5 9.23 5 10.045V10.54C5 10.6233 4.99458 10.7067 4.98375 10.79C4.94125 11.0975 4.78875 12.2412 4.64625 13.4275C4.50125 14.6337 4.375 15.82 4.375 16.25C4.375 16.5815 4.5067 16.8995 4.74112 17.1339C4.97554 17.3683 5.29348 17.5 5.625 17.5C5.95652 17.5 6.27446 17.3683 6.50888 17.1339C6.7433 16.8995 6.875 16.5815 6.875 16.25C6.875 15.82 6.75 14.6337 6.60375 13.4263C6.46125 12.2413 6.30875 11.0975 6.26625 10.7887C6.25674 10.7066 6.25132 10.624 6.25 10.5412V10.0462C6.25 9.23125 6.77625 8.605 7.325 8.24875C7.76259 7.96505 8.12222 7.57635 8.37112 7.11807C8.62002 6.65979 8.75027 6.14651 8.75 5.625C8.75 4.46 8.54 3.42 8.36875 2.76875C8.33125 2.625 8.1875 2.5 7.98125 2.5C7.85361 2.5 7.73121 2.5507 7.64095 2.64095C7.5507 2.73121 7.5 2.85361 7.5 2.98125V6.25ZM11.25 6.875C11.25 5.38316 11.8426 3.95242 12.8975 2.89752C13.9524 1.84263 15.3832 1.25 16.875 1.25C17.0408 1.25 17.1997 1.31585 17.3169 1.43306C17.4342 1.55027 17.5 1.70924 17.5 1.875V9.34125L17.5238 9.5625C17.6232 10.4954 17.7186 11.4288 17.81 12.3625C17.9638 13.9325 18.125 15.6925 18.125 16.25C18.125 16.913 17.8616 17.5489 17.3928 18.0178C16.9239 18.4866 16.288 18.75 15.625 18.75C14.962 18.75 14.3261 18.4866 13.8572 18.0178C13.3884 17.5489 13.125 16.913 13.125 16.25C13.125 15.6925 13.2863 13.9325 13.44 12.3625C13.5188 11.5662 13.5975 10.8038 13.6562 10.2387L13.6812 10H12.5C12.1685 10 11.8505 9.8683 11.6161 9.63388C11.3817 9.39946 11.25 9.08152 11.25 8.75V6.875ZM14.9963 9.44125L14.97 9.69375C14.8723 10.6239 14.7773 11.5543 14.685 12.485C14.5262 14.0938 14.375 15.7725 14.375 16.25C14.375 16.5815 14.5067 16.8995 14.7411 17.1339C14.9755 17.3683 15.2935 17.5 15.625 17.5C15.9565 17.5 16.2745 17.3683 16.5089 17.1339C16.7433 16.8995 16.875 16.5815 16.875 16.25C16.875 15.7712 16.7238 14.0938 16.565 12.485C16.4733 11.5542 16.3783 10.6238 16.28 9.69375L16.2537 9.4425L16.25 9.375V2.54375C15.2086 2.69407 14.2562 3.21469 13.5674 4.01019C12.8787 4.80569 12.4997 5.82277 12.5 6.875V8.75H14.375C14.4626 8.75003 14.5493 8.7685 14.6293 8.8042C14.7094 8.8399 14.781 8.89203 14.8396 8.95722C14.8982 9.02241 14.9424 9.09919 14.9694 9.18258C14.9964 9.26597 15.0055 9.3541 14.9963 9.44125Z" fill="#262831"/></svg>'
    },
    {
        "id": 3,
        "title": "Technology",
        "icon": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M17.2518 12.49C16.9678 14.855 15.4188 15.8 14.7498 16.486C14.0798 17.174 14.1998 17.311 14.2448 18.32C14.2523 18.4448 14.2341 18.5699 14.1915 18.6875C14.1488 18.805 14.0825 18.9126 13.9967 19.0036C13.9109 19.0945 13.8074 19.167 13.6925 19.2164C13.5776 19.2658 13.4538 19.2912 13.3288 19.291H10.6708C10.5458 19.2908 10.4222 19.2651 10.3074 19.2155C10.1927 19.166 10.0893 19.0935 10.0035 19.0027C9.91767 18.9118 9.85127 18.8044 9.80834 18.687C9.7654 18.5697 9.74683 18.4448 9.75376 18.32C9.75376 17.33 9.84576 17.1 9.24976 16.486C8.48976 15.726 6.70176 14.653 6.70176 11.702C6.6972 10.969 6.84453 10.243 7.13448 9.56977C7.42442 8.89654 7.85069 8.29067 8.38641 7.79035C8.92213 7.29004 9.55569 6.90613 10.2471 6.66283C10.9386 6.41952 11.673 6.3221 12.4039 6.3767C13.1349 6.43129 13.8467 6.63673 14.4943 6.98005C15.142 7.32338 15.7115 7.79715 16.1669 8.37149C16.6224 8.94584 16.9539 9.60831 17.1406 10.3171C17.3273 11.026 17.3652 11.7658 17.2518 12.49Z" stroke="#262831" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M10.46 19.236V20.748C10.46 21.161 10.69 21.5 10.973 21.5H13.026C13.311 21.5 13.54 21.16 13.54 20.748V19.236M11.22 8.696C10.6295 8.69626 10.0633 8.93101 9.64588 9.34863C9.22845 9.76624 8.99396 10.3325 8.99396 10.923M19.332 11.904H21.166M17.486 5.892L18.787 4.591M18.486 17L19.787 18.3M12 2.377V3.86M5.23996 4.59L6.53196 5.892M4.23996 18.3L5.53196 17M4.66796 11.904H2.83496" stroke="#262831" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    }
]
