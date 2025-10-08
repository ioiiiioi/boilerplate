# TODO: Remove Project-Specific Email Templates

These email templates are specific to a school admission system (SPMB/PPDB) and should NOT be in a generic Django boilerplate:

## Files to Delete:
1. `notify_applicant_result_failed.txt` - School admission rejection email (in Indonesian)
2. `notify_applicant_result_passed.txt` - School admission acceptance email (in Indonesian)  
3. `registration_confirmation_ppdb.txt` - School registration confirmation email (in Indonesian)

## What to Do:
- **DELETE** these files completely from the boilerplate
- If you need email templates, create generic ones like:
  - `password_reset.html` (keep the existing one)
  - `welcome_email.html`
  - `verification_email.html`
  
These are project-specific and pollute the boilerplate with business logic.

