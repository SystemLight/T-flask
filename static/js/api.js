const service = axios.create({
    baseURL: "/api"
});

service.interceptors.request.use(config => {
    const token = localStorage.getItem("token");
    if (token) {
        config.headers["Authorization"] = "Bearer " + localStorage.getItem("token");
    }
    return config;
});

service.interceptors.response.use(response => {
    return response;
}, (err) => {
    if (err.response) {
        if (err.response.status === 401) {
            // 当返回401即代表token失效，所以删除本地所有令牌存储即可
            console.log("token失效")
        }
    }

    return Promise.reject(err);
});

async function upload(url, file, onProcess) {
    const chunkSize = 3145728;
    const fileSize = file.size;
    let currentChunk = 0;
    const totalChunks = Math.ceil(fileSize / chunkSize);
    const formID = uuidv1();
    let result = {};

    for (; currentChunk < totalChunks; currentChunk++) {
        const offset = currentChunk * chunkSize;
        const currentChunkSize = (currentChunk + 1) * chunkSize;

        const fd = new FormData();
        fd.append("chunkBlock", file.slice(offset, currentChunkSize));
        fd.append("fileName", file.name);
        fd.append("fileID", formID);
        fd.append("fileSize", fileSize);
        fd.append("offset", offset);
        fd.append("chunkID", currentChunk);
        fd.append("totalChunks", totalChunks);

        const {data} = await axios.post(url, fd);
        result = data;

        onProcess && onProcess(parseInt((currentChunk / totalChunks) * 100), fd);
    }

    return result;
}
