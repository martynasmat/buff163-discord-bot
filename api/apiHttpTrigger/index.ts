import { AzureFunction, Context, HttpRequest } from "@azure/functions";

type RequestBody = {
    mode: 0 | 1;
    arg: string;
    float?: number;
    pattern?: string;
    discord_id: string;
    margin: string;
};

const httpTrigger: AzureFunction = async function (
    context: Context,
    req: HttpRequest
): Promise<void> {
    const request: RequestBody = req.body;

    if (
        !request.mode ||
        !request.arg ||
        !request.margin ||
        !request.discord_id
    ) {
        console.log("Incorrect input parameters.");
    } else {
        context.res = {
            body: `${JSON.stringify(request)}`,
        };
    }
};

export default httpTrigger;
