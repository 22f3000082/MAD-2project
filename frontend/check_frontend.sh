#!/bin/bash
set -e

echo "🔍 Running comprehensive frontend checks..."

# Check node and npm versions
echo "📋 Checking Node.js environment..."
node -v
npm -v

# Install dependencies if needed
echo "📦 Checking dependencies..."
if [ ! -d "node_modules" ] || [ ! -f "node_modules/.package-lock.json" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Run ESLint to find code problems
echo "🔎 Running ESLint for code quality issues..."
npx eslint src/ --ext .js,.vue --max-warnings=0 || {
    echo "⚠️ ESLint found issues. Please fix them before proceeding."
    exit 1
}

# Check for dependency vulnerabilities
echo "🔒 Checking for dependency vulnerabilities..."
npm audit || echo "⚠️ Some vulnerabilities found. Consider running npm audit fix"

# Check for outdated packages
echo "📅 Checking for outdated packages..."
npm outdated || echo "⚠️ Some packages are outdated. Consider updating them."

# Run unit tests if they exist
echo "🧪 Running unit tests..."
if grep -q "test" package.json; then
    npm run test || echo "⚠️ Tests failed. Please fix failing tests."
else
    echo "⚠️ No test script found in package.json. Consider adding tests."
fi

# Build the application to catch compilation errors
echo "🏗️ Building application to catch compilation errors..."
npm run build || {
    echo "❌ Build failed. Please fix build errors."
    exit 1
}

# Check for console.log statements that might have been left in production code
echo "🔍 Checking for unwanted console.log statements..."
grep -r "console.log" src/ --include="*.vue" --include="*.js" | grep -v "// Debug" && echo "⚠️ Found console.log statements that might need to be removed before production." || echo "✅ No unwanted console.log statements found."

# Check for TODO comments in the code
echo "📝 Checking for TODO comments..."
grep -r "TODO" src/ --include="*.vue" --include="*.js" && echo "⚠️ Found TODO comments that might need to be addressed." || echo "✅ No TODO comments found."

# Validate api endpoints used in the application
echo "🌐 Validating API endpoints..."
grep -r "api\." src/ --include="*.vue" --include="*.js" | sort | uniq
echo "⚠️ Please manually verify that these API endpoints exist in the backend."

# Check for unused components or dead code
echo "🧹 Checking for potential unused components..."
for file in $(find src/components -name "*.vue"); do
    component_name=$(basename "$file" .vue)
    if ! grep -q "$component_name" --include="*.vue" --include="*.js" src/; then
        echo "⚠️ Potential unused component: $file"
    fi
done

echo "✅ Frontend checks completed!" 