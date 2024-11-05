"use client";

import { Dispatch, SetStateAction, useEffect, useState } from "react";
import Select, { components, OptionProps, SingleValueProps } from 'react-select';

type Option = {
    value: string;
    label: string;
    svgIcon: string;
};

type GroupedOption = {
    label: string;
    options: Option[];
};

const CustomOption = (props: OptionProps<Option>) => {
    return (
        <components.Option {...props}>
            <div style={{
                display: "flex",
                gap: "1rem",
                alignItems: "center",
            }}>
                <span
                    style={{ width: 10, height: 30, marginRight: 10 }}
                    dangerouslySetInnerHTML={{ __html: props.data.svgIcon }}
                />
                {props.data.label}
            </div>
        </components.Option>
    );
};

const CustomSingleValue = (props: SingleValueProps<Option>) => {
    return (
        <components.SingleValue {...props}>
            <div style={{
                display: "flex",
                gap: "1rem",
                alignItems: "center",
            }}>
                <span
                    style={{ width: 10, height: 30, marginRight: 10 }}
                    dangerouslySetInnerHTML={{ __html: props.data.svgIcon }}
                />
                {props.data.label}
            </div>
        </components.SingleValue>
    );
};

interface KnowledgeBaseSelectBoxProps {
    onChange: Dispatch<SetStateAction<string | undefined>>;
}

export default function KnowledgeBaseSelectBox({ onChange }: KnowledgeBaseSelectBoxProps) {
    const [groupedOptions, setGroupedOptions] = useState<GroupedOption[]>([]);
    const [isLoaded, setIsLoaded] = useState(false);

    useEffect(() => {
        fetch(process.env.NEXT_PUBLIC_API_SERVER_URL + "/get_knowledge_bases?user_id=1")
            .then((res) => res.json())
            .then((data) => {
                const newOptions: Option[] = data.map((item: any) => ({
                    value: item.id,
                    label: item.title,
                    svgIcon: item.icon,
                }));

                const grouped: GroupedOption[] = [
                    {
                        label: "SELECT KNOWLEDGE BASE",
                        options: newOptions,
                    }
                ];

                setGroupedOptions(grouped);
                setIsLoaded(true);
            });
    }, []);

    if (!isLoaded) {
        return <div>Loading...</div>;
    }

    return (
        <Select
            options={groupedOptions}
            components={{ Option: CustomOption, SingleValue: CustomSingleValue }}
            defaultValue={groupedOptions[0]?.options[0]}
            onChange={(selected) => {
                if (selected) {
                    // @ts-expect-error Necessary due to not type from object.
                    onChange(selected.label)
                }
            }}
            styles={{
                control: (base) => ({
                    ...base,
                    width: "100%",
                    background: "var(--background-opacity-70)",
                }),
                menu: (base) => ({
                    ...base,
                    background: "var(--background-opacity-70)",
                    backdropFilter: "blur(10px)",
                }),
            }}
        />
    );
}
