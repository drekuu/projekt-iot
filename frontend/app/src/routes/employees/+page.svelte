<script>
import { onMount } from 'svelte';
let employees = [];
let editEmployeeId;
let maxBalance = 200;
let formData = {
    id: '',
    firstName: '',
    lastName: ''
}

let bonusData = {
    worker_id: '',
    bonus: 0
}
const baseUrl = "http://localhost:5173/api"
const workersUrl = "http://localhost:5173/api/workers"

onMount(async ()=>{
    employees = await getEmployeesData();
});

async function getEmployeesData(){
    try{
        const response = await fetch(workersUrl);
        const data = await response.json();
        const result = Object.keys(data).map(key => {
            const entry = data[key];
            return {
                worker_id: key,
                card_id: entry.card_id,
                first_name: entry.first_name,
                last_name: entry.last_name,
                balance: entry.balance
            }
        })
        return result;
    }catch(err){
        console.log(err);
    }
}

async function addEmployee(){
    if(!formData.id){
        console.log('invalid input');
        return;
    }
    let data = {firstname: formData.firstName, lastname: formData.lastName, card: formData.id}
    try{
        const queryParams = new URLSearchParams(data);
        const url = `/addworker?${queryParams.toString()}`
        const response = await fetch(baseUrl + url, {
            method: "POST", 
            headers: {
                'Content-Type': 'application/json',
            }, 
            body: JSON.stringify(data)
        })
        if(response.ok){
            console.log("Form data sent successfully");
        }else{
            console.error("error sending form data", response.status);
        }
    }catch(e){
        console.log(e)
    }
    formData = {
        id: '',
        firstName: '',
        lastName: ''
    }
}

async function editBalance(){
    if(bonusData.bonus == null) bonusData.bonus = 0.0
    try{
        const url = `/addbalance/${bonusData.worker_id}?value=${bonusData.bonus}`
        const response = await fetch(baseUrl + url, {
            method: "POST", 
            headers: {
                'Content-Type': 'application/json',
            },
        })
        if(response.ok){
            console.log("Form data sent successfully");
        }else{
            console.error("error sending form data", response.status);
        }
    }catch(e){
        console.log(e);
    }
}

</script>

<div class=" p-5 flex flex-col items-center gap-5">
    <h1 class=" text-xl"><strong>Employees List</strong></h1>
    <table class=" w-4/6 text-lg border-collapse border-solid border-black border-2">
        <tr>
            <th>Worker ID</th>
            <th>Card ID</th>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Balance</th>
        </tr>
        {#each employees as employee}
            <tr class="">
                <td>{employee.worker_id}</td>
                <td>{employee.card_id}</td>
                <td>{employee.first_name}</td>
                <td>{employee.last_name}</td>
                <td>
                <div class=" flex flex-row justify-between gap-4">
                    <h2 class=" border-2 border-white">
                        {employee.balance}
                    </h2> 
                </div>
                </td>
            </tr>
        {/each}
    </table>


    <div class=" flex flex-col justify-center items-center gap-5">
        <h1 class=" text-xl"><strong>Add New Employee</strong></h1>
        <form on:submit|preventDefault={addEmployee} id="add_form" class="flex flex-col justify-center items-center gap-3">
            <table>
                <tr>
                    <td>
                        <input type="text" placeholder="Card ID" id="card_id" name="card_id" bind:value={formData.id}>
                        <label for="card_id" class=" hidden">Card Id</label>
                    </td>  
                    <td>
                        <input type="text" placeholder="First Name" id="name" name="firstName" bind:value={formData.firstName}>
                        <label for="name" class=" hidden">First Name</label>
                    </td>
                    <td>
                        <input type="text" placeholder="Last Name" id="lastname" name="lastName" bind:value={formData.lastName}>
                    <label for="lastname" class=" hidden">Last Name</label>
                    </td>
                       
                </tr>
            </table>
            <button type="submit">
                <i class="fa-solid fa-circle-plus text-4xl"></i>
            </button>
        </form>
        
    </div>

    <div class=" flex flex-col justify-center items-center gap-5">
        <h1 class=" text-xl"><strong>Increase Worker's Balance</strong></h1>
        <form on:submit|preventDefault={editBalance} id="add_form" class="flex flex-col justify-center items-center gap-3">
            <table>
                <tr>
                    <td>
                        <input type="text" placeholder="Card ID" id="card_id" name="card_id" bind:value={bonusData.worker_id}>
                        <label for="card_id" class=" hidden">Card Id</label>
                    </td>  
                    <td>
                        <input type="number" placeholder="Bonus Value" id="bonus" name="bonus" bind:value={bonusData.bonus}>
                        <label for="bonus" class=" hidden">Bonus Value</label>
                    </td> 
                </tr>
            </table>
            <button type="submit">
                <i class="fa-solid fa-circle-plus text-4xl"></i>
            </button>
        </form>
        
    </div>


</div>

<style lang="postcss">
table, th, td {
    border: 1px solid;
}
td{
    padding: 4px;
}
</style>