from enum import Enum


class URLS(Enum):
    login = "/api/auth/login"
    get_access_token = "/api/accounts/user/get_auth_token"
    challenge_details = "/api/challenges/challenge/{}"
    make_submission = "/api/jobs/challenge/{}/challenge_phase/{}/submission/"
    get_aws_credentials = (
        "/api/challenges/phases/{}/participant_team/aws/credentials/"
    )
    download_file = "/api/jobs/submission_files/?bucket={}&key={}"
    phase_details_using_slug = "/api/challenges/phase/{}/"
    get_presigned_url_for_annotation_file = "/api/challenges/phases/{}/get_annotation_file_presigned_url/"
    get_presigned_url_for_submission_file = "/api/jobs/phases/{}/get_submission_file_presigned_url/"
    finish_upload_for_submission_file = "/api/jobs/phases/{}/finish_submission_file_upload/{}/"
    finish_upload_for_annotation_file = "/api/challenges/phases/{}/finish_annotation_file_upload/"
    send_submission_message = "/api/jobs/phases/{}/send_submission_message/{}/"
