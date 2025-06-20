import {HMClient, type OpenAPIConfig} from "hospital-manager-client";

export const DEFAULT_CLIENT_CONFIG: OpenAPIConfig = {
    BASE: "", // Only API path will be used Django's endpoint will be routed by default
    VERSION: "",
    WITH_CREDENTIALS: true,
    CREDENTIALS: "include"
}

export const backendClient: HMClient = new HMClient(DEFAULT_CLIENT_CONFIG)