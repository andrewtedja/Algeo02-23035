"use client";

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
import { useState } from "react";

export default function SearchAlbum() {
	// MOCK DATA
	const mockData = Array.from({ length: 50 }, (_, index) => ({
		id: index + 1,
		title: `Song Title ${index + 1}`,
		artist: `Artist ${index + 1}`,
	}));

	const [currentPage, setCurrentPage] = useState(1);
	const itemsPerPage = 10;
	const totalPages = Math.ceil(mockData.length / itemsPerPage);
	const indexOfLastItem = currentPage * itemsPerPage;
	const indexOfFirstItem = indexOfLastItem - itemsPerPage;
	const currentItems = mockData.slice(indexOfFirstItem, indexOfLastItem);

	const handlePageChange = (pageNumber) => {
		if (pageNumber < 1 || pageNumber > totalPages) return;
		setCurrentPage(pageNumber);
	};

	const handlePrevious = () => {
		handlePageChange(currentPage - 1);
	};

	const handleNext = () => {
		handlePageChange(currentPage + 1);
	};

	////////////////////////////////////////////////

	const [selectedFile, setSelectedFile] = useState(null);
	const [uploadMessage, setUploadMessage] = useState(null);
	const [uploadError, setUploadError] = useState(null);

	const handleFileChange = (event) => {
		const file = event.target.files[0];
		setSelectedFile(file);
		setUploadMessage(null);
		setUploadError(null);
	};

	const uploadFile = async (file) => {
		setUploadError(null);
		setUploadMessage(null);
		try {
			const formData = new FormData();
			formData.append("file", file);

			const response = await fetch("http://localhost:8000/upload/album", {
				method: "POST",
				body: formData,
			});

			if (!response.ok) {
				throw new Error("Failed to upload album cover");
			}

			const data = await response.json();
			setUploadMessage(data.message);
		} catch (err) {
			throw err;
		}
	};

	const handleSearch = () => {
		if (selectedFile) {
			uploadFile(selectedFile);
		}
	};

	return (
		<Layout title="Album Finder">
			<div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
				<div className="flex items-center justify-between mb-8">
					<h1 className="text-4xl font-extrabold text-gray-900 flex items-center gap-3">
						<Images className="text-emerald-500" size={40} />
						Search by Album
					</h1>
					<Button className="hover:bg-black hover:text-white transition duration-500">
						<Search className="mr-2" /> Search
					</Button>
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
								className="text-emerald-500 group-hover:text-emerald-600 
								transition-colors duration-300"
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
						<Upload className="mr-2" /> Upload Image
					</Button>
					{uploadMessage && (
						<p className="text-green-600 mt-2">{uploadMessage}</p>
					)}
					{uploadError && (
						<p className="text-red-600 mt-2">{uploadError}</p>
					)}
				</div>

				{/* MOCK RESULTS */}
				<div className="mb-8">
					<div className="flex justify-between items-center mb-4">
						<h2 className="text-3xl font-bold text-gray-900">
							Search Results
						</h2>
						<p className="text-muted-foreground">
							Runtime: 0.342 seconds
						</p>
					</div>

					<div className="grid grid-cols-4 lg:grid-cols-5 gap-6">
						{[...Array(10)].map((_, i) => (
							<Card
								key={i}
								className="overflow-hidden hover:shadow-md
								transition-all duration-100 transform cursor-pointer
								hover:-translate-y-2 border-2 border-transparent 
								border-slate-300"
							>
								<div className="aspect-square relative group">
									<Image
										src="/placeholder.svg"
										alt="Album cover"
										layout="fill"
										objectFit="cover"
										className="transition-transform duration-300 group-hover:scale-110"
									/>
								</div>
								<div className="p-5">
									<h3 className="font-bold text-xl text-gray-900 mb-1">
										Album Title
									</h3>
									<p className="text-muted-foreground mb-2">
										Artist Name
									</p>
									<Badge
										variant="secondary"
										className="bg-slate-100 text-slate-800"
									>
										Match: 94.6%
									</Badge>
								</div>
							</Card>
						))}
					</div>
				</div>

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
									onClick={() => handlePageChange(index + 1)}
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
			</div>
		</Layout>
	);
}
