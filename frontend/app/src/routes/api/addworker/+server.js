import { json } from '@sveltejs/kit';

export async function POST(requestEvent){
    const { request } = requestEvent;
    const data = await request.json();
    console.log(data);
    return json(data, { status: 201 });
}