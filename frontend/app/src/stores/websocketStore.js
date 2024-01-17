import websocketStore from "svelte-websocket-store";

const initialValue = {};
export const socket = websocketStore("", initialValue, ["1"]);

