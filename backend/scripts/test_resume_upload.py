"""
Test resume upload and extraction flow
"""
import requests
import json
from pathlib import Path

BASE_URL = "http://localhost:8000/api/v1"

def test_resume_flow():
    """
    Test complete resume upload and extraction flow
    """
    print("🧪 Testing Resume Upload & Extraction Flow\n")

    # 1. Create a new profile first
    print("1️⃣  Creating new student profile...")
    create_response = requests.post(
        f"{BASE_URL}/profiles/create",
        json={
            "name": "Test Student",
            "email": "test@example.com"
        }
    )

    if create_response.status_code != 200:
        print(f"❌ Failed to create profile: {create_response.text}")
        return

    profile_data = create_response.json()
    student_id = profile_data['data']['id']
    print(f"✅ Created profile with ID: {student_id}\n")

    # 2. Upload resume PDF
    print("2️⃣  Uploading resume PDF...")
    pdf_path = Path(__file__).parent.parent / "test_data" / "sample_resume.pdf"

    with open(pdf_path, 'rb') as f:
        files = {'file': ('sample_resume.pdf', f, 'application/pdf')}
        upload_response = requests.post(
            f"{BASE_URL}/profiles/upload-resume?student_id={student_id}",
            files=files
        )

    if upload_response.status_code != 200:
        print(f"❌ Failed to upload resume: {upload_response.text}")
        return

    upload_data = upload_response.json()
    print(f"✅ Resume uploaded successfully!")
    print(f"   - Filename: {upload_data['data']['filename']}")
    print(f"   - Text length: {upload_data['data']['text_length']} chars")
    print(f"   - Preview: {upload_data['data']['text_preview'][:100]}...\n")

    # 3. Extract profile data using AI
    print("3️⃣  Extracting profile data with AI...")
    extract_response = requests.post(
        f"{BASE_URL}/profiles/extract-from-resume/{student_id}"
    )

    if extract_response.status_code != 200:
        print(f"❌ Failed to extract profile: {extract_response.text}")
        return

    extracted_data = extract_response.json()['data']
    print(f"✅ Profile extracted successfully!")
    print(f"   - Name: {extracted_data['name']}")
    print(f"   - Email: {extracted_data['email']}")
    print(f"   - GPA: {extracted_data['gpa']}")
    print(f"   - Skills: {', '.join(extracted_data['skills'][:5])}...")
    print(f"   - Education: {len(extracted_data['education'])} entries")
    print(f"   - Work Experience: {len(extracted_data['work_experience'])} entries")
    print(f"   - Confidence: {extracted_data['extraction_confidence']:.0%}\n")

    # 4. Get full profile
    print("4️⃣  Retrieving complete profile...")
    get_response = requests.get(f"{BASE_URL}/profiles/{student_id}")

    if get_response.status_code != 200:
        print(f"❌ Failed to get profile: {get_response.text}")
        return

    full_profile = get_response.json()['data']
    print(f"✅ Full profile retrieved!")
    print(f"   - Profile source: {full_profile['profile_source']}")
    print(f"   - Activities: {', '.join(full_profile['activities'][:3]) if full_profile['activities'] else 'None'}")
    print(f"   - Achievements: {', '.join(full_profile['achievements'][:2]) if full_profile['achievements'] else 'None'}")
    print(f"   - Languages: {', '.join(full_profile['languages']) if full_profile['languages'] else 'None'}")
    print(f"   - Certifications: {', '.join(full_profile['certifications']) if full_profile['certifications'] else 'None'}\n")

    # 5. Test essay generation with extracted profile
    print("5️⃣  Testing essay generation with extracted profile...")

    # Get a scholarship
    scholarships_response = requests.get(f"{BASE_URL}/demo/scholarships")
    scholarship_id = scholarships_response.json()['scholarships'][0]['id']

    # Generate essay
    essay_response = requests.post(
        f"{BASE_URL}/demo/generate-essay",
        json={
            "scholarship_id": scholarship_id,
            "student_id": student_id
        }
    )

    if essay_response.status_code != 200:
        print(f"❌ Failed to generate essay: {essay_response.text}")
        return

    essay_data = essay_response.json()['data']
    print(f"✅ Essay generated successfully!")
    print(f"   - Type: {essay_data['type']}")
    print(f"   - Alignment Score: {essay_data['alignment_score']}")
    print(f"   - Paragraphs: {len(essay_data['paragraphs'])}")
    print(f"   - First paragraph preview: {essay_data['paragraphs'][0]['content'][:150]}...")

    print("\n✨ All tests passed successfully!")
    print(f"📊 Profile extraction confidence: {extracted_data['extraction_confidence']:.0%}")

    # Cleanup
    print("\n🧹 Cleaning up test data...")
    delete_response = requests.delete(f"{BASE_URL}/profiles/{student_id}/resume")
    if delete_response.status_code == 200:
        print("✅ Test data cleaned up")


if __name__ == "__main__":
    test_resume_flow()