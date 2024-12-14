"use client";

import { useState } from "react";
import { Layout } from "@/components/layout";
import { Button } from "@/components/ui/button";
import { Upload, Music, Search } from "lucide-react";

export default function SearchAudioPage() {
	const [selectedDataset, setSelectedDataset] = useState(null);
	const [selectedMapper, setSelectedMapper] = useState(null);

	const handleDatasetChange = (event) => {
		const file = event.target.files[0];
		setSelectedDataset(file);
	};

	const handleMapperChange = (event) => {
		const file = event.target.files[0];
		setSelectedMapper(file);
	};

	return (
		<Layout title="Music Information Retrieval">
			<div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
				<div className="flex items-center justify-between mb-8">
					<h1 className="text-4xl font-extrabold text-gray-900 flex items-center gap-3">
						<Music className="text-sky-500" size={40} />
						Search by Audio
					</h1>
				</div>

				{/* Dataset */}
				<div className="mb-8">
					<h2 className="text-2xl font-bold mb-4">Upload Dataset</h2>
					<div
						className="border-2 border-dashed border-violet-200 bg-violet-50/50 
						rounded-2xl p-8 text-center transition-all duration-100 
						hover:border-violet-400 hover:bg-violet-50 
						group cursor-pointer relative"
					>
						<input
							type="file"
							accept="audio/*"
							className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
							onChange={handleDatasetChange}
						/>
						<div className="flex flex-col items-center justify-center space-y-4">
							<Upload
								className="text-violet-500 group-hover:text-violet-600 
								transition-colors duration-300"
								size={64}
								strokeWidth={1.5}
							/>
							<h3 className="text-xl font-semibold text-gray-800">
								{selectedDataset
									? `Selected: ${selectedDataset.name}`
									: "Drag and Drop || Click to Upload Dataset"}
							</h3>
							<p className="text-muted-foreground">
								Supports WAV/MIDI Files
							</p>
						</div>
					</div>
				</div>

				{/* Mapper */}
				<div className="mb-8">
					<h2 className="text-2xl font-bold mb-4">Upload Mapper</h2>
					<div
						className="border-2 border-dashed border-red-200 bg-red-50/50 
						rounded-2xl p-8 text-center transition-all duration-100 
						hover:border-red-400 hover:bg-red-50 
						group cursor-pointer relative"
					>
						<input
							type="file"
							accept="application/json"
							className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
							onChange={handleMapperChange}
						/>
						<div className="flex flex-col items-center justify-center space-y-4">
							<Upload
								className="text-red-500 group-hover:text-red-600 
								transition-colors duration-300"
								size={64}
								strokeWidth={1.5}
							/>
							<h3 className="text-xl font-semibold text-gray-800">
								{selectedMapper
									? `Selected: ${selectedMapper.name}`
									: "Drag and Drop || Click to Upload Mapper"}
							</h3>
							<p className="text-muted-foreground">
								Supports JSON Files
							</p>
						</div>
					</div>
				</div>

				{/* Button */}
				<Button
					size="lg"
					className="mt-4"
					disabled={!selectedDataset || !selectedMapper}
				>
					<Search className="mr-2" /> Search Song
				</Button>
			</div>
		</Layout>
	);
}
