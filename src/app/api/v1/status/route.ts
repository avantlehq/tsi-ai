import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const jobId = searchParams.get('jobId')
    const tenantId = searchParams.get('tenantId')

    if (!jobId) {
      return NextResponse.json(
        { error: 'Missing required parameter: jobId' },
        { status: 400 }
      )
    }

    // Mock status check
    const statusResult = {
      jobId,
      type: jobId.startsWith('tsi_') ? 'conversion' : 'validation',
      status: getRandomStatus(),
      progress: Math.floor(Math.random() * 100),
      estimatedTimeRemaining: Math.floor(Math.random() * 30000) + 5000,
      currentStep: getCurrentStep(jobId),
      steps: [
        { name: 'parsing', status: 'completed', duration: 1200 },
        { name: 'validation', status: 'in_progress', duration: null },
        { name: 'conversion', status: 'pending', duration: null },
        { name: 'packaging', status: 'pending', duration: null }
      ],
      metrics: {
        recordsProcessed: Math.floor(Math.random() * 1000) + 100,
        totalRecords: Math.floor(Math.random() * 1000) + 500,
        errorsFound: Math.floor(Math.random() * 5),
        warningsFound: Math.floor(Math.random() * 10)
      },
      timestamps: {
        started: new Date(Date.now() - Math.floor(Math.random() * 300000)).toISOString(),
        lastUpdate: new Date().toISOString()
      }
    }

    return NextResponse.json({
      success: true,
      data: statusResult
    })
  } catch (error) {
    console.error('Status check error:', error)
    return NextResponse.json(
      { error: 'Internal server error during status check' },
      { status: 500 }
    )
  }
}

function getRandomStatus() {
  const statuses = ['queued', 'in_progress', 'completed', 'failed']
  const weights = [0.1, 0.6, 0.25, 0.05] // Higher chance for in_progress
  
  const random = Math.random()
  let cumulativeWeight = 0
  
  for (let i = 0; i < statuses.length; i++) {
    cumulativeWeight += weights[i]
    if (random <= cumulativeWeight) {
      return statuses[i]
    }
  }
  
  return 'in_progress'
}

function getCurrentStep(jobId: string) {
  const conversionSteps = ['Parsing input data', 'Validating structure', 'Converting format', 'Generating output']
  const validationSteps = ['Parsing input data', 'Running validation rules', 'Analyzing results', 'Generating report']
  
  const steps = jobId.startsWith('tsi_') ? conversionSteps : validationSteps
  return steps[Math.floor(Math.random() * steps.length)]
}