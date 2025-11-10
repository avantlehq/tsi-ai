import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { 
      inputData, 
      format,
      validationLevel = 'standard',
      tenantId 
    } = body

    if (!inputData || !format) {
      return NextResponse.json(
        { error: 'Missing required fields: inputData, format' },
        { status: 400 }
      )
    }

    const supportedFormats = ['json-transport', 'edifact', 'gtfs']
    if (!supportedFormats.includes(format)) {
      return NextResponse.json(
        { error: `Unsupported format. Supported: ${supportedFormats.join(', ')}` },
        { status: 400 }
      )
    }

    // Mock validation process
    const validationResult = {
      jobId: `val_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      format,
      validationLevel,
      status: 'completed',
      isValid: true,
      summary: {
        totalRecords: Array.isArray(inputData) ? inputData.length : Object.keys(inputData).length,
        validRecords: Array.isArray(inputData) ? inputData.length - 1 : Object.keys(inputData).length - 1,
        errors: generateMockErrors(format),
        warnings: generateMockWarnings(format),
        notices: generateMockNotices(format)
      },
      details: {
        fieldValidation: {
          required: { passed: 95, failed: 2, percentage: 97.9 },
          format: { passed: 97, failed: 0, percentage: 100 },
          range: { passed: 90, failed: 7, percentage: 92.8 }
        },
        dataIntegrity: {
          consistency: { score: 98.5, issues: 1 },
          completeness: { score: 96.2, missing: 3 },
          accuracy: { score: 99.1, outliers: 2 }
        }
      },
      recommendations: generateRecommendations(format),
      metadata: {
        validationEngine: 'TSI-Validator-v1.0',
        processingTime: Math.floor(Math.random() * 3000) + 500,
        timestamp: new Date().toISOString()
      }
    }

    return NextResponse.json({
      success: true,
      data: validationResult
    })
  } catch (error) {
    console.error('Validation error:', error)
    return NextResponse.json(
      { error: 'Internal server error during validation' },
      { status: 500 }
    )
  }
}

function generateMockErrors(format: string) {
  const baseErrors = [
    {
      code: 'MISSING_REQUIRED_FIELD',
      message: 'Required field "route_id" is missing',
      line: 23,
      field: 'route_id',
      severity: 'error'
    }
  ]

  if (format === 'gtfs') {
    return [
      ...baseErrors,
      {
        code: 'INVALID_TIME_FORMAT',
        message: 'Time format should be HH:MM:SS',
        line: 45,
        field: 'arrival_time',
        severity: 'error'
      }
    ]
  }

  return baseErrors.slice(0, Math.floor(Math.random() * 2))
}

function generateMockWarnings(format: string) {
  const warnings = [
    {
      code: 'UNUSUAL_VALUE',
      message: 'Route distance seems unusually high (>1000km)',
      line: 12,
      field: 'route_distance',
      severity: 'warning'
    },
    {
      code: 'MISSING_OPTIONAL_FIELD',
      message: 'Optional field "route_color" not specified',
      line: 18,
      field: 'route_color',
      severity: 'warning'
    }
  ]

  return warnings.slice(0, Math.floor(Math.random() * 3))
}

function generateMockNotices(format: string) {
  return [
    {
      code: 'INFO',
      message: `Successfully processed ${format.toUpperCase()} data`,
      severity: 'info'
    },
    {
      code: 'OPTIMIZATION_TIP',
      message: 'Consider adding route descriptions for better usability',
      severity: 'info'
    }
  ]
}

function generateRecommendations(format: string) {
  const recommendations = [
    'Add missing required fields to improve data completeness',
    'Standardize time formats across all entries',
    'Consider adding route descriptions for better user experience'
  ]

  if (format === 'gtfs') {
    recommendations.push('Validate stop coordinates against real-world locations')
    recommendations.push('Ensure service calendars cover the intended operational period')
  }

  return recommendations.slice(0, Math.floor(Math.random() * 4) + 1)
}