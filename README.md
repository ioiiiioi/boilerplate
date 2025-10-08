# Django REST Framework Boilerplate

<!-- TODO: Update README with proper boilerplate documentation -->
<!-- The project name "e-masjid" is project-specific and should be removed from boilerplate -->

## Issues to Fix Before Using This Boilerplate

### Critical Bugs
1. **Missing comma** - Fixed in `core/auth/backend.py` line 57
2. **Wrong model reference** - `core/base/base_models.py` references `users.User` but should be `user.User`
3. **Missing method** - `apps/user/serializers.py` calls undefined `add_google_info()` method
4. **Incomplete URL config** - `core/urls.py` doesn't include API routes

### Files to Delete (All commented out code)
- `core/auth/views.py` - Completely commented out
- `core/auth/serializers.py` - Completely commented out  
- `utils/middleware/cut_off_middleware.py` - Completely commented out
- `utils/middleware/storages_middleware.py` - Completely commented out
- `core/templates/email/notify_applicant_result_*.txt` - Project-specific email templates
- `core/templates/email/registration_confirmation_ppdb.txt` - Project-specific

### Code to Clean Up
- Remove project-specific references to: `school`, `school_id`, `is_deleted`, `session_login_id`, `gender` fields
- Add missing settings: `IS_SINGLE_LOGIN` or remove related code
- Remove unused `LoggingViewMixins` class or implement it
- Clean up `apps/user/tests.py` or add actual tests

### Docker Issues
- `docker-compose..yaml` has double dots in filename (should be `docker-compose.yaml`)
- Missing Dockerfile referenced in docker-compose

See individual files for detailed TODO comments.