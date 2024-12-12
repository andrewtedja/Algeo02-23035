import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
	AlertDialog,
	AlertDialogAction,
	AlertDialogCancel,
	AlertDialogContent,
	AlertDialogDescription,
	AlertDialogFooter,
	AlertDialogHeader,
	AlertDialogTitle,
} from "@/components/ui/alert-dialog";

interface UploadFormProps {
	title: string;
	buttonText: string;
	onUpload: (file: File) => void;
}

export function UploadForm({ title, buttonText, onUpload }: UploadFormProps) {
	const [showCancelAlert, setShowCancelAlert] = useState(false);
	const [selectedFile, setSelectedFile] = useState<File | null>(null);

	const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		const file = e.target.files?.[0];
		if (file) {
			setSelectedFile(file);
		}
	};

	const handleUpload = () => {
		if (selectedFile) {
			onUpload(selectedFile);
		}
	};

	return (
		<div className="space-y-6">
			<h1 className="text-2xl font-bold">{title}</h1>

			<div className="grid place-items-center gap-4 p-8 bg-muted/40 rounded-lg">
				<Input
					type="file"
					className="max-w-sm"
					onChange={handleFileChange}
					accept="audio/*,image/*"
				/>
				<div className="flex gap-2">
					<Button
						size="lg"
						onClick={handleUpload}
						disabled={!selectedFile}
					>
						{buttonText}
					</Button>
					<Button
						size="lg"
						variant="outline"
						onClick={() => setShowCancelAlert(true)}
					>
						Cancel
					</Button>
				</div>
			</div>

			<AlertDialog
				open={showCancelAlert}
				onOpenChange={setShowCancelAlert}
			>
				<AlertDialogContent>
					<AlertDialogHeader>
						<AlertDialogTitle>
							Are you sure you want to cancel?
						</AlertDialogTitle>
						<AlertDialogDescription>
							This will clear your current upload progress.
						</AlertDialogDescription>
					</AlertDialogHeader>
					<AlertDialogFooter>
						<AlertDialogCancel>Back</AlertDialogCancel>
						<AlertDialogAction
							onClick={() => {
								setSelectedFile(null);
								setShowCancelAlert(false);
							}}
						>
							Yes, cancel
						</AlertDialogAction>
					</AlertDialogFooter>
				</AlertDialogContent>
			</AlertDialog>
		</div>
	);
}
