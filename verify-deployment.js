#!/usr/bin/env node

// Deployment readiness verification script
const fs = require('fs');
const path = require('path');

console.log('🔍 Verifying deployment readiness...\n');

const checks = [];

// Check essential files exist
const requiredFiles = [
    'server.js',
    'package.json',
    'railway.json',
    'customer_mapping_data.json',
    'public/index.html'
];

requiredFiles.forEach(file => {
    if (fs.existsSync(path.join(__dirname, file))) {
        checks.push({ name: `✅ ${file}`, status: 'PASS' });
    } else {
        checks.push({ name: `❌ ${file}`, status: 'FAIL' });
    }
});

// Check package.json dependencies
try {
    const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
    const requiredDeps = ['express', 'cors', 'express-basic-auth'];
    
    requiredDeps.forEach(dep => {
        if (pkg.dependencies && pkg.dependencies[dep]) {
            checks.push({ name: `✅ Dependency: ${dep}`, status: 'PASS' });
        } else {
            checks.push({ name: `❌ Dependency: ${dep}`, status: 'FAIL' });
        }
    });

    // Check start script
    if (pkg.scripts && pkg.scripts.start === 'node server.js') {
        checks.push({ name: '✅ Start script configured', status: 'PASS' });
    } else {
        checks.push({ name: '❌ Start script missing', status: 'FAIL' });
    }
} catch (e) {
    checks.push({ name: '❌ package.json invalid', status: 'FAIL' });
}

// Check data file size (should be substantial)
try {
    const stats = fs.statSync('customer_mapping_data.json');
    const sizeMB = (stats.size / (1024 * 1024)).toFixed(1);
    if (stats.size > 100000) { // > 100KB
        checks.push({ name: `✅ Customer data (${sizeMB}MB)`, status: 'PASS' });
    } else {
        checks.push({ name: `❌ Customer data too small (${sizeMB}MB)`, status: 'FAIL' });
    }
} catch (e) {
    checks.push({ name: '❌ Customer data file error', status: 'FAIL' });
}

// Check git status
try {
    const { execSync } = require('child_process');
    const gitStatus = execSync('git status --porcelain', { encoding: 'utf8' });
    if (gitStatus.trim() === '') {
        checks.push({ name: '✅ Git repository clean', status: 'PASS' });
    } else {
        checks.push({ name: '⚠️ Uncommitted changes', status: 'WARN' });
    }
} catch (e) {
    checks.push({ name: '❌ Git not initialized', status: 'FAIL' });
}

// Display results
console.log('📋 Deployment Readiness Report:\n');
checks.forEach(check => {
    console.log(check.name);
});

const failCount = checks.filter(c => c.status === 'FAIL').length;
const warnCount = checks.filter(c => c.status === 'WARN').length;
const passCount = checks.filter(c => c.status === 'PASS').length;

console.log(`\n📊 Summary: ${passCount} passed, ${warnCount} warnings, ${failCount} failed\n`);

if (failCount === 0) {
    console.log('🎉 All checks passed! Ready for Railway deployment.');
    console.log('👉 Next steps:');
    console.log('   1. Push to GitHub: git push origin main');
    console.log('   2. Visit https://railway.app');
    console.log('   3. Deploy from GitHub repo');
    console.log('   4. Set APP_PASSWORD environment variable');
    console.log('   5. Test your live URL!\n');
} else {
    console.log('❌ Some checks failed. Please fix these issues before deploying.\n');
}