<script>
import { onMount } from 'svelte';
let employees = [];
let editEmployeeId;
let maxBalance = 200;
let formData = {
    id: '',
    firstName: '',
    lastName: '',
    balance: ''
}
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

function updateEmployeeBalance(employeeId, newBalance){
    const id = employees.findIndex(employee => employee.card_id === employeeId)
    if(id !== -1){
        const updatedEmployees = employees;
        updatedEmployees[id].balance = newBalance;
        employees = updatedEmployees; 
    }
}

function addEmployee(){
    if(!formData.id){
        console.log('invalid input');
        return;
    }
    employees = [...employees, {id: formData.id,
                                first_name: formData.firstName,
                                lastName: formData.lastName, 
                                balance: formData.balance}]
    let form = document.getElementById('add_form');
    form?.reset;
    formData = {
        id: '',
        firstName: '',
        lastName: '',
        balance: ''
    }
}

</script>

<div class=" p-5 flex flex-col items-center gap-5">
    <h1 class=" text-xl"><strong>Employees List</strong></h1>
    <table class=" w-4/6 text-lg border-collapse border-solid border-black border-2">
        <tr>
            <th>Card ID</th>
            <th>First Name</th>
            <th>Last Name</th>
            <th class="">Balance</th>
        </tr>
        {#each employees as employee}
            <tr class="">
                <td>{employee.card_id}</td>
                <td>{employee.first_name}</td>
                <td>{employee.last_name}</td>
                <td>
                <div class=" flex flex-row justify-between px-2">

                    {#if editEmployeeId !== employee.card_id}
                        <h2 class=" w-10 border-2 border-white">
                            {employee.balance}
                        </h2>
                        <button on:click={()=> editEmployeeId = employee.card_id}>
                            <i class="fa-solid fa-pen-to-square"></i>
                        </button>
                    {:else}
                        <input class=" w-10 border-2 rounded-md" type="number" id="{employee.card_id}" value="{employee.balance}">
                        <button on:click={()=>{
                            let balanceVal = document.getElementById(employee.card_id)?.value;
                            if(balanceVal > maxBalance) balanceVal = maxBalance;
                            updateEmployeeBalance(employee.card_id, balanceVal);
                            editEmployeeId = '';
                        }}>
                            <i class="fa-solid fa-upload"></i>
                        </button>    
                    {/if}
                </div>
                </td>
            </tr>
        {/each}
    </table>


    <div class=" flex flex-col justify-center items-center gap-5">
        <h1 class=" text-xl"><strong>Add New Employee</strong></h1>
        <form action="" id="add_form">
            <table>
                <tr>
                    <td>
                        <input class="" type="text" placeholder="Id" id="id" name="id" bind:value={formData.id}>
                        <label for="id" class=" hidden">Id</label>
                    </td>
                    <td>
                        <input type="text" placeholder="First Name" id="name" name="firstName" bind:value={formData.first_name}>
                        <label for="name" class=" hidden">First Name</label>
                    </td>
                    <td>
                        <input type="text" placeholder="Last Name" id="lastname" name="lastName" bind:value={formData.lastName}>
                    <label for="lastname" class=" hidden">Last Name</label>
                    </td>
                    <td>
                        <input type="value" placeholder="Balance" id="form_balance" name="balance" bind:value={formData.balance}>
                        <label for="form_balance" class=" hidden">Balance</label>
                    </td>             
                </tr>
            </table>
            
        </form>
        <button on:click={addEmployee}>
            <i class="fa-solid fa-circle-plus text-4xl"></i>
        </button>
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