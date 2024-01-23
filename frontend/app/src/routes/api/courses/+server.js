export const GET = () => {
    return new Response(JSON.stringify({
        Course1: ["Stop1", "Stop2", "Stop3"],
        Course2: ["Stop4", "Stop5", "Stop6", "Stop7", "Stop8", "Stop9", "Stop10", "Stop11", "Stop12", "Stop13"]
        }), { status: 200});
}