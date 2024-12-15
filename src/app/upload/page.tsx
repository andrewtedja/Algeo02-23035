"use client";

import { useState } from "react";
import { Layout } from "@/components/layout";
import { Button } from "@/components/ui/button";
import { Upload, Music, Braces } from "lucide-react";

export default function SearchAudioPage() {
	const [selectedDataset, setSelectedDataset] = useState(null);
	const [selectedMapper, setSelectedMapper] = useState(null);

	const [datasetUploaded, setDatasetUploaded] = useState(false);
	const [mapperUploaded, setMapperUploaded] = useState(false);
	const [uploadError, setUploadError] = useState(null);

	const handleDatasetChange = (event) => {
		const file = event.target.files[0];
		setSelectedDataset(file);
		setDatasetUploaded(false);
	};

	const handleMapperChange = (event) => {
		const file = event.target.files[0];
		setSelectedMapper(file);
		setMapperUploaded(false);
	};

	const uploadFile = async (file, endpoint) => {
		setUploadError(null);
		try {
			const formData = new FormData();
			formData.append("file", file);

			const response = await fetch(
				`http://localhost:8000/upload/${endpoint}`,
				{
					method: "POST",
					body: formData,
				}
			);
			if (!response.ok) {
				throw new Error(`Failed to upload ${endpoint}`);
			}
			const data = await response.json();
			return data;
		} catch (err) {
			throw err;
		}
	};

	const uploadDataset = async () => {
		if (!selectedDataset) return;
		try {
			const res = await uploadFile(selectedDataset, "dataset");
			alert(res.message);
			setDatasetUploaded(true);
		} catch (err) {
			console.error(err);
		}
	};

	const uploadMapper = async () => {
		if (!selectedMapper) return;
		try {
			const res = await uploadFile(selectedMapper, "mapper");
			alert(res.message);
			setMapperUploaded(true);
		} catch (err) {
			console.error(err);
		}
	};

	return (
		<Layout title="Upload">
			<div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
				<div className="mb-8">
					<div className="flex items-center justify-between mb-8">
						<h2 className="text-4xl font-extrabold text-gray-900 flex items-center gap-3">
							<Braces className="text-violet-500" size={40} />
							Upload Dataset/Mapper
						</h2>
					</div>
					<div
						className="border-2 border-dashed border-violet-200 bg-violet-50/50 
							rounded-2xl p-8 text-center transition-all duration-100 
							hover:border-violet-400 hover:bg-violet-50 
							group cursor-pointer relative"
					>
						<input
							type="file"
							accept=".zip"
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
									: "Drag and Drop || Click to Upload Dataset (ZIP)"}
							</h3>
							<p className="text-muted-foreground">
								Upload a zip file containing your dataset.
							</p>
						</div>
					</div>
					<Button
						className="mt-4 hover:bg-gray-900 transition-colors duration-300 hover:text-white"
						onClick={uploadDataset}
					>
						<Upload className="mr-2" />
						{datasetUploaded
							? "Dataset Uploaded"
							: "Upload Dataset"}
					</Button>
				</div>

				<div className="mb-8">
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
									: "Drag and Drop || Click to Upload Mapper (JSON)"}
							</h3>
							<p>Upload a JSON file that maps your dataset.</p>
						</div>
					</div>
					<Button
						className="mt-4 hover:bg-gray-900 transition-colors duration-300 hover:text-white"
						onClick={uploadMapper}
					>
						<Upload className="mr-2" />
						{mapperUploaded ? "Mapper Uploaded" : "Upload Mapper"}
					</Button>
				</div>

				{uploadError && (
					<div className="text-red-500 mb-4">
						Error: {uploadError}
					</div>
				)}

				<Button
					className="mt-4 hover:bg-dark hover:text-white"
					disabled={!datasetUploaded || !mapperUploaded}
				>
					Search Song
				</Button>
			</div>
		</Layout>
	);
}
