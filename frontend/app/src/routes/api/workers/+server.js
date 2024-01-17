export const GET = () => {
    return new Response(JSON.stringify({1: {
                                            first_name: "Jan",
                                            last_name: "Kowalski",
                                            balance: 10,
                                            card_id: "12312"
                                        },
                                        2: {
                                            first_name: "Mateusz",
                                            last_name: "Kowalski",
                                            balance: 50,
                                            card_id: "12345"
                                        }
    }), { status: 200});
}