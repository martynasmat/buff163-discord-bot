import { createConnection, QueryError } from "mysql2";
import { AzureFunction, Context, HttpRequest } from "@azure/functions";

import "./loadenv";

type RequestBody = {
    mode: 0 | 1;
    arg: string;
    float: number;
    pattern: string;
    discord_id: string;
    margin: string;
};

type CSItem = {
    ID: number;
    goods_id: string;
    item_name: string;
    item_name_formatted: string;
};

function get_id_from_url(url: string): string {
    // returns the goods_id value from provided buff.163.com market url
    return url.match(/(goods\/)([0-9]+)/)[2];
}

async function insert_tracker(request: RequestBody): Promise<void> {
    const connection = createConnection(process.env.DATABASE_URL as string);
    const { discord_id, float, pattern, margin } = request;

    const { ID, goods_id, item_name, item_name_formatted }: CSItem = (
        await connection
            .promise()
            .execute("SELECT * from buff_items WHERE goods_id = ? LIMIT 1;", [
                get_id_from_url(request.arg),
            ])
    )[0][0];

    await connection
        .promise()
        .execute(
            `INSERT INTO buff_tracker (item_name, item_name_formatted, goods_id, discord_id, float_value, pattern_id, margin) VALUES (?,?,?,?,?,?,?);`,
            [
                item_name,
                item_name_formatted,
                goods_id,
                discord_id,
                float,
                pattern,
                margin,
            ]
        );

    connection.end();
}

const httpTrigger: AzureFunction = async function (
    context: Context,
    req: HttpRequest
): Promise<void> {
    const request: RequestBody = req.body;
    const params = [
        "mode",
        "arg",
        "margin",
        "discord_id",
        "float",
        "margin",
        "pattern",
    ];

    for (const param of params) {
        if (request[param]) continue;

        context.res = {
            status: 400,
            body: JSON.stringify({ message: `Missing ${param} parameter.` }),
        };

        return;
    }

    await insert_tracker(request);

    context.res = {
        status: 201,
        body: JSON.stringify({
            message: "Item tracker was added successfully.",
        }),
    };
};

export default httpTrigger;
