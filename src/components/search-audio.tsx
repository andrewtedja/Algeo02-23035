"use client";

import Image from "next/image";
import { Layout } from "@/components/layout";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Upload, Music, Search } from "lucide-react";
import {
	Pagination,
	PaginationContent,
	PaginationItem,
	PaginationLink,
	PaginationNext,
	PaginationPrevious,
} from "@/components/ui/pagination";
import { useState } from "react";

export default function SearchAudio() {
	const [selectedFile, setSelectedFile] = useState<File | null>(null);
	const [uploadMessage, setUploadMessage] = useState<string | null>(null);
	const [uploadError, setUploadError] = useState<string | null>(null);

	const [searchResults, setSearchResults] = useState<any[]>([]);
	const [searchRuntime, setSearchRuntime] = useState<number | null>(null);

	const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
		const file = event.target.files?.[0] || null;
		setSelectedFile(file);
		setUploadMessage(null);
		setUploadError(null);
	};

	const handleSearch = async () => {
		if (!selectedFile) {
			return;
		}
		setUploadError(null);
		setUploadMessage(null);

		try {
			const formData = new FormData();
			formData.append("file", selectedFile);
			const response = await fetch("http://localhost:8000/search/audio", {
				method: "POST",
				body: formData,
			});
			if (!response.ok) {
				throw new Error("Search failed.	");
			}
			const data = await response.json();
			setSearchResults(data.results);
			setSearchRuntime(data.runtime);
		} catch (err) {
			throw err;
		}
	};

	///////////////////// PAGINATION /////////////////////
	const itemsPerPage = 10;
	const totalPages = Math.ceil(searchResults.length / itemsPerPage);
	const [currentPage, setCurrentPage] = useState(1);
	const indexOfLastItem = currentPage * itemsPerPage;
	const indexOfFirstItem = indexOfLastItem - itemsPerPage;
	const currentItems = searchResults.slice(indexOfFirstItem, indexOfLastItem);

	const handlePageChange = (pageNumber: number) => {
		if (pageNumber < 1 || pageNumber > totalPages) return;
		setCurrentPage(pageNumber);
	};

	return (
		<Layout title="Search by Audio">
			<div className="max-w-6xl mx-auto px-4 py-12">
				<div className="flex justify-between items-center mb-8">
					<h1 className="text-4xl font-bold flex items-center gap-3">
						<Music className="text-sky-500" size={40} />
						Search Audio
					</h1>
					<Button
						disabled={!selectedFile}
						onClick={handleSearch}
						className="bg-blue-600 hover:bg-blue-700 text-white"
					>
						<Search className="mr-2" /> Search
					</Button>
				</div>

				<div className="mb-12">
					<div className="border-dashed border-2 rounded-lg p-6 bg-sky-50 text-center">
						<input
							type="file"
							accept="audio/*"
							className="hidden"
							id="file-input"
							onChange={handleFileChange}
						/>
						<label htmlFor="file-input" className="cursor-pointer">
							<Upload className="text-sky-500" size={64} />
							<p>
								{selectedFile
									? selectedFile.name
									: "Upload an audio file (WAV, MIDI)"}
							</p>
						</label>
					</div>
				</div>

				{searchResults.length > 0 && (
					<>
						<div className="mb-4">
							<h2 className="text-3xl font-bold">
								Search Results
							</h2>
							<p>
								Runtime:{" "}
								{searchRuntime
									? `${searchRuntime.toFixed(3)} seconds`
									: "N/A"}
							</p>
						</div>

						<div className="grid grid-cols-4 gap-6">
							{currentItems.map((result, index) => (
								<Card key={index} className="p-4">
									<h3 className="font-bold text-lg">
										{result.audio_name || "Unknown Audio"}
									</h3>
									<p>
										Matched with:{" "}
										{result.image_name || "No Image"}
									</p>
									<Badge className="bg-green-100 text-green-800">
										Match:{" "}
										{(result.similarity * 100).toFixed(2)}%
									</Badge>
								</Card>
							))}
						</div>

						<Pagination>
							<PaginationContent>
								<PaginationPrevious
									onClick={() =>
										handlePageChange(currentPage - 1)
									}
									disabled={currentPage === 1}
								/>
								{Array.from({ length: totalPages }, (_, i) => (
									<PaginationItem key={i + 1}>
										<PaginationLink
											onClick={() =>
												handlePageChange(i + 1)
											}
											isActive={i + 1 === currentPage}
										>
											{i + 1}
										</PaginationLink>
									</PaginationItem>
								))}
								<PaginationNext
									onClick={() =>
										handlePageChange(currentPage + 1)
									}
									disabled={currentPage === totalPages}
								/>
							</PaginationContent>
						</Pagination>
					</>
				)}

				{uploadError && <p className="text-red-600">{uploadError}</p>}
			</div>
		</Layout>
	);
}
