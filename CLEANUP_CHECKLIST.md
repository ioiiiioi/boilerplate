# Django Boilerplate Cleanup Checklist

This document lists all issues found in the boilerplate that need to be addressed.

## 🔴 Critical Bugs (Must Fix)

### 1. ✅ Missing Comma (FIXED)
- **File**: `core/auth/backend.py` line 57
- **Issue**: Missing comma after `"id"` in fields list
- **Status**: FIXED - comma added

### 2. Wrong Model Reference
- **File**: `core/base/base_models.py` line 22
- **Issue**: References `"users.User"` but should be `"user.User"`
- **Action**: Change `"users.User"` to `"user.User"` OR remove `UserCreatorModels` if not needed

### 3. Missing Method Call
- **File**: `apps/user/serializers.py` line 95
- **Issue**: Calls undefined `self.add_google_info(instance)` method
- **Action**: Define the method or remove the line

### 4. Incomplete URL Configuration
- **File**: `core/urls.py`
- **Issue**: Doesn't include API routes, only admin
- **Action**: Add API URLs and documentation endpoints (see TODO comments in file)

---

## 🗑️ Files to Delete (All Code Commented Out)

1. **`core/auth/views.py`** - Entire file is commented out
2. **`core/auth/serializers.py`** - Entire file is commented out
3. **`utils/middleware/cut_off_middleware.py`** - Entire file is commented out
4. **`utils/middleware/storages_middleware.py`** - Entire file is commented out (also missing S3 dependencies)

---

## 📧 Project-Specific Files to Remove

### Email Templates (School Admission System)
- `core/templates/email/notify_applicant_result_failed.txt`
- `core/templates/email/notify_applicant_result_passed.txt`
- `core/templates/email/registration_confirmation_ppdb.txt`

These are Indonesian language templates for a school admission system (PPDB/SPMB) and don't belong in a generic boilerplate.

---

## 🧹 Code to Clean Up

### Project-Specific Field References
The following fields are referenced but don't exist in the base User model:

#### In `apps/user/serializers.py`:
- `gender` (line 26)
- `school_id` (line 29, 66)
- `school` (line 37)
- `user_type` (line 38, 53)

#### In `core/auth/backend.py`:
- `school` (line 99, 100)
- `session_login_id` (line 118)
- `is_deleted` (line 295)

**Action Options**:
1. Add these fields to the User model if needed
2. Remove all references to them from serializers/backend

### Unused Code
1. **`LoggingViewMixins`** in `utils/api/generics.py` - Defined but never used
2. **`CacheManager`** in `utils/cache/cache_manager.py` - Defined but never used
3. **`merge_response_dicts()`** in `utils/api/schema.py` - Defined but never used

**Action**: Remove if not needed, or implement usage

### Empty/Placeholder Files
1. **`apps/user/tests.py`** - Only has placeholder comment
2. **`apps/user/admin.py`** - User model not registered (TODO comment added)

---

## ⚙️ Configuration Issues

### Missing Settings
- `IS_SINGLE_LOGIN` - Referenced in `core/auth/backend.py` line 103 but not defined in settings
  - **Action**: Add to settings or remove the feature

### Incorrect Settings
- `DEFAULT_VERSION = "v2"` in `core/settings/base.py` but only `core/urls/v1.py` exists
  - **Action**: Verify which version is correct

### Commented Out Settings
- Pagination: `"DEFAULT_PAGINATION_CLASS"` (line 200)
- Throttling: `"DEFAULT_THROTTLE_RATES"` (line 211-214)
  - Includes project-specific `"applicant_signup"` rate

---

## 🔒 Security Issues

### 1. Insecure ALLOWED_HOSTS
- **File**: `core/settings/base.py` line 32
- **Issue**: `ALLOWED_HOSTS = ["*"]` allows all hosts
- **Action**: Configure specific domains for production

### 2. Insecure CORS Settings
- **File**: `core/settings/base.py` line 36
- **Issue**: `CORS_ORIGIN_ALLOW_ALL = True` allows all origins
- **Action**: Set to `False` and configure `CORS_ALLOWED_ORIGINS` in production

---

## 🐳 Docker Issues

### 1. Filename Error
- **File**: `docker-compose..yaml` (double dots)
- **Action**: Rename to `docker-compose.yaml`

### 2. Missing Dockerfile
- **Issue**: `docker-compose..yaml` references `build: .` but no Dockerfile exists
- **Action**: Create Dockerfile

### 3. Missing Database Service
- **Issue**: Settings require PostgreSQL but docker-compose only has Redis
- **Action**: Add PostgreSQL service to docker-compose

---

## 📦 Project Naming Issues

### 1. Project Name
- **File**: `pyproject.toml` line 2
- **Issue**: Named "e-masjid" (project-specific)
- **Action**: Change to generic boilerplate name

### 2. README
- **File**: `README.md` line 1
- **Issue**: Title is "e-masjid" (project-specific)
- **Action**: Update with proper boilerplate documentation

---

## 📋 Summary Statistics

- **Critical Bugs**: 4 (1 fixed, 3 remaining)
- **Files to Delete**: 7
- **Unused Code Definitions**: 3
- **Security Issues**: 2
- **Configuration Issues**: 4
- **Docker Issues**: 3
- **Naming Issues**: 2

---

## ✅ Quick Action Plan

1. **Immediate (Critical)**:
   - Fix model reference in `core/base/base_models.py`
   - Fix or remove `add_google_info()` call in serializers
   - Complete URL configuration in `core/urls.py`

2. **Cleanup (High Priority)**:
   - Delete all commented-out files
   - Remove project-specific email templates
   - Decide on and remove unused field references

3. **Configuration**:
   - Add missing `IS_SINGLE_LOGIN` setting or remove feature
   - Fix Docker setup (rename file, add Dockerfile, add PostgreSQL)
   - Configure security settings for production

4. **Polish**:
   - Remove unused code (LoggingViewMixins, CacheManager, etc.)
   - Update project naming throughout
   - Write proper README documentation
   - Add tests or clean up test files

---

## 📝 Notes

- Most TODO comments have been added throughout the codebase
- Some features (like school management, Google OAuth) appear to be partially implemented
- Consider creating a `dev` and `prod` settings split
- Consider adding environment-specific configurations

