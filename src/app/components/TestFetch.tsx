"use client";

import React, { useEffect, useState } from "react";

type ApiResponse = {
	message: string; // Define the expected structure of the API response
};

export default function TestFetch() {
	const [data, setData] = useState<ApiResponse | null>(null); // Use the type here
	const [error, setError] = useState(false);

	useEffect(() => {
		fetch("http://localhost:8000/api/hello") // Update the port to 8000
			.then((response) => response.json())
			.then((data: ApiResponse) => setData(data)) // Explicitly type the response
			.catch(() => setError(true));
	}, []);

	return (
		<div style={{ textAlign: "center", marginTop: "50px" }}>
			<h1>FastAPI Fetch Test</h1>
			{error ? (
				<p style={{ color: "red" }}>Failed to connect to FastAPI.</p>
			) : data ? (
				<p>{data.message}</p>
			) : (
				<p>Loading...</p>
			)}
		</div>
	);
}
