const axios = require('axios');

const filters = [
    { key: "name", op: "contains", value: "John" },
    { key: "status", op: "eq", value: "Active" }
];

axios.post('http://localhost:5000/api/users', filters, {
    params: {
        page: 1,
        per_page: 10,
        sort_by: 'name',
        order: 'asc'
    }
})
.then(response => {
    console.log(JSON.stringify(response.data, null, 2));
})
.catch(error => {
    console.error("Error fetching data:", error);
});
