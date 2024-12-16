"use client";

import { useState } from "react";
import Image from "next/image";
import { Layout } from "@/components/layout";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Upload, Images, Search } from "lucide-react";
import {
	Pagination,
	PaginationContent,
	PaginationItem,
	PaginationLink,
	PaginationNext,
	PaginationPrevious,
} from "@/components/ui/pagination";

export default function SearchAlbum() {
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

			const response = await fetch("http://localhost:8000/search/album", {
				method: "POST",
				body: formData,
			});

			if (!response.ok) {
				throw new Error("Search failed.");
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

	const handlePrevious = () => {
		handlePageChange(currentPage - 1);
	};

	const handleNext = () => {
		handlePageChange(currentPage + 1);
	};

	return (
		<Layout title="Album Finder">
			<div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
				<div className="flex items-center justify-between mb-8">
					<h1 className="text-4xl font-extrabold text-gray-900 flex items-center gap-3">
						<Images className="text-emerald-500" size={40} />
						Search by Album
					</h1>
				</div>

				<div className="mb-12">
					<div
						className="border-2 border-dashed border-emerald-200 bg-emerald-50/50 
						rounded-2xl p-8 text-center transition-all duration-100 
						hover:border-emerald-400 hover:bg-emerald-50 
						group cursor-pointer relative"
					>
						<input
							type="file"
							accept="image/*"
							className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
							onChange={handleFileChange}
						/>
						<div className="flex flex-col items-center justify-center space-y-4">
							<Upload
								className="text-emerald-500 group-hover:text-emerald-600 transition-colors duration-300"
								size={64}
								strokeWidth={1.5}
							/>
							<h2 className="text-2xl font-semibold text-gray-800">
								{selectedFile
									? `Selected: ${selectedFile.name}`
									: "Drag and Drop || Click to Upload Album Cover"}
							</h2>
							<p className="text-muted-foreground">
								Supports JPG/PNG Files
							</p>
						</div>
					</div>
					<Button
						size="lg"
						className="mt-4 hover:bg-slate-900 hover:text-white"
						disabled={!selectedFile}
						onClick={handleSearch}
					>
						<Upload className="mr-2" /> Upload &amp; Search
					</Button>
					{uploadMessage && (
						<p className="text-green-600 mt-2">{uploadMessage}</p>
					)}
					{uploadError && (
						<p className="text-red-600 mt-2">{uploadError}</p>
					)}
				</div>

				{searchResults.length > 0 && (
					<div className="mb-8">
						<div className="flex justify-between items-center mb-4">
							<h2 className="text-3xl font-bold text-gray-900">
								Search Results
							</h2>
							<p className="text-muted-foreground">
								Runtime:{" "}
								{searchRuntime
									? `${searchRuntime.toFixed(3)} seconds`
									: "N/A"}
							</p>
						</div>

						<div className="grid grid-cols-4 lg:grid-cols-5 gap-3">
							{currentItems.map((item: any, i: number) => (
								<Card
									key={i}
									className="overflow-hidden hover:shadow-md transition-all duration-100 transform cursor-pointer hover:-translate-y-2 border-2 border-transparent border-slate-300"
								>
									<div className="aspect-square relative group">
										<Image
											src={`http://localhost:8000/images/${item.image_name}`}
											alt="Album cover"
											layout="fill"
											objectFit="cover"
											className="transition-transform duration-300 group-hover:scale-110"
										/>
									</div>
									<div className="p-5">
										<h3 className="font-bold text-xs text-gray-900 mb-1 break-words">
											{item.image_name || "Unknown Image"}
										</h3>
										<p className="text-muted-foreground text-sm mb-2">
											{item.audio_name ||
												"No corresponding audio"}
										</p>
										<Badge
											variant="secondary"
											className="bg-amber-100 text-slate-800"
										>
											Match:{" "}
											{(item.similarity * 100).toFixed(2)}
											%
										</Badge>
									</div>
								</Card>
							))}
						</div>
					</div>
				)}

				{searchResults.length > 0 && totalPages > 1 && (
					<Pagination className="cursor-pointer">
						<PaginationContent>
							<PaginationItem>
								<PaginationPrevious
									onClick={handlePrevious}
									disabled={currentPage === 1}
								/>
							</PaginationItem>
							{Array.from({ length: totalPages }, (_, index) => (
								<PaginationItem key={index + 1}>
									<PaginationLink
										onClick={() =>
											handlePageChange(index + 1)
										}
										isActive={currentPage === index + 1}
									>
										{index + 1}
									</PaginationLink>
								</PaginationItem>
							))}
							<PaginationItem>
								<PaginationNext
									onClick={handleNext}
									disabled={currentPage === totalPages}
								/>
							</PaginationItem>
						</PaginationContent>
					</Pagination>
				)}
			</div>
		</Layout>
	);
}
