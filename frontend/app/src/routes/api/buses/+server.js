export const GET = () => {
    return new Response(JSON.stringify({1: {
                                            course_name: "Course1",
                                            stop_number: 3,
                                            direction: "right"
                                        },
                                        2: {
                                            course_name: "Course2",
                                            stop_number: 5,
                                            direction: "right"
                                        }
    }), { status: 200});
}